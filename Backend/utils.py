from io import BytesIO
from transformers import CLIPProcessor, CLIPModel

import cv2, os
import numpy as np
import torch
from PIL import Image
from scipy.stats import entropy
from timm import create_model
from torchvision import transforms
from huggingface_hub import hf_hub_download
from dotenv import load_dotenv
load_dotenv()

# Get Hugging Face token from environment variable
token = os.getenv("HF_HUB_TOKEN")
if token is None:
    raise ValueError("Hugging Face token not found. Please set the 'HF_HUB_TOKEN' environment variable.")

# To check if an image is AI-generated or not
ai_vs_human_model_path = hf_hub_download(
    repo_id="ateeqdafi/ai-image-detection",
    filename="model_epoch_8_acc_0.9859.pth",
    use_auth_token=token
)

# Parameters
IMG_SIZE = 380  # Size for EfficientNet-B4
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
LABEL_MAPPING = {1: "human", 0: "ai"}  # Class labels

# Image preprocessing (same as training)
transform = transforms.Compose([
    transforms.Resize(IMG_SIZE + 20),  # Resize slightly larger to allow for cropping
    transforms.CenterCrop(IMG_SIZE),  # Crop to the desired size
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # Normalization
])

# Load the model
model = create_model('efficientnet_b4', pretrained=False, num_classes=2)  # Two-class classification
model.load_state_dict(torch.load(ai_vs_human_model_path, map_location=DEVICE))  # Load trained weights
model = model.to(DEVICE)
model.eval()  # Set to evaluation mode

def predict_single_image(
    image: Image.Image,
    model: torch.nn.Module,
    transform: transforms.Compose,
    device: torch.device
):
    try:
        # Preprocess image
        image_tensor = transform(image).unsqueeze(0)  # Add batch dimension

        # Perform inference
        image_tensor = image_tensor.to(device)
        with torch.no_grad():
            logits = model(image_tensor)  # Get logits
            probs = torch.nn.functional.softmax(logits, dim=1)  # Apply softmax to get class probabilities
            predicted_class = torch.argmax(probs, dim=1).item()  # Get the predicted class (0 or 1)
            confidence = probs[0, predicted_class].item()  # Confidence of the predicted class

        result = {
                'status': LABEL_MAPPING[predicted_class],
                'score': confidence
            }
        return result
    except Exception as e:
        print(f"Error predicting image: {e}")
        raise

def is_ai_generated(file_bytes: bytes) -> bool:
    try:
        # Process image
        img = Image.open(BytesIO(file_bytes)).convert("RGB")

        # Make prediction
        label = predict_single_image(img, model, transform, DEVICE)
        # logger.info(f"Predicted label: {label}, Confidence: {confidence:.2f}")
        return label
    except Exception as e:
        print(f"Error predicting AI-generated image: {e}")
        return False

def image_quality(image_bytes: bytes) -> bool:
    try:
        # Convert bytes to numpy array
        image_array = np.frombuffer(image_bytes, np.uint8)

        # Decode the image
        img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        if img is None:
            print("Rejected: Image could not be decoded.")
            return False

        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        results = {}

        # 1. Blur Detection
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        results['blur_score'] = laplacian_var

        # Portrait Detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        is_portrait = len(faces) > 0

        # Adjust blur threshold for portraits
        blur_threshold = 30 if is_portrait else 60
        normalized_blur = min(laplacian_var / blur_threshold, 1.0)

        # 2. Image Quality Metrics
        height, width = img.shape[:2]
        resolution = height * width
        results['resolution'] = resolution

        brightness = np.mean(gray)
        results['brightness'] = brightness

        contrast = np.std(gray)
        results['contrast'] = contrast

        # 3. Motion Blur Detection
        dft = np.fft.fft2(gray)
        dft_shift = np.fft.fftshift(dft)
        magnitude_spectrum = 20 * np.log(np.abs(dft_shift) + 1e-8)  # Add epsilon to prevent log(0)
        motion_blur_score = np.std(magnitude_spectrum)
        results['motion_blur'] = motion_blur_score

        # 4. Significance Analysis
        edges = cv2.Canny(gray, 100, 200)
        edge_density = np.sum(edges > 0) / gray.size
        results['edge_density'] = edge_density

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        color_std_dev = np.mean([np.std(hsv[:, :, i]) for i in range(3)])
        results['color_std_dev'] = color_std_dev

        # Entropy Analysis
        hist, _ = np.histogram(gray.ravel(), bins=256, range=[0, 256])
        entropy_value = entropy(hist, base=2)
        results['entropy'] = entropy_value

        # Adjust weight for blur dynamically based on portrait detection
        blur_weight = 0.05 if is_portrait else 0.2
        redistributed_weight = 0.15 if is_portrait else 0.0  # Remaining weight to redistribute

        # Final Scoring Weights
        weights = {
            'blur_score': 0.1 + blur_weight,
            'resolution': 0.15 + (redistributed_weight / 3),
            'brightness': 0.1,
            'contrast': 0.05,
            'motion_blur': 0.05,
            'edge_density': 0.25 + (redistributed_weight / 3),
            'color_std_dev': 0.15 + (redistributed_weight / 3),
            'entropy': 0.15
        }

        # Normalize metrics
        normalized_resolution = min(resolution / 1_000_000, 1.0)
        normalized_brightness = min(brightness / 255, 1.0)
        normalized_contrast = min(contrast / 255, 1.0)
        normalized_motion_blur = min(motion_blur_score / 100, 1.0)
        normalized_edge_density = min(edge_density / 0.05, 1.0)
        normalized_color_std_dev = min(color_std_dev / 100, 1.0)
        normalized_entropy = min(entropy_value / 8.0, 1.0)

        # Compute final score
        final_score = (
            weights['blur_score'] * normalized_blur +
            weights['resolution'] * normalized_resolution +
            weights['brightness'] * normalized_brightness +
            weights['contrast'] * normalized_contrast +
            weights['motion_blur'] * normalized_motion_blur +
            weights['edge_density'] * normalized_edge_density +
            weights['color_std_dev'] * normalized_color_std_dev +
            weights['entropy'] * normalized_entropy
        )
        
        results['final_score'] = final_score
        if final_score < 0.65:
            quality = "Low"
        elif final_score < 0.85:
            quality = "Medium"
        else:
            quality = "High"
        # is_low_quality = final_score < 0.6
        results['is_low_quality'] = quality

        return {
            'status': str(quality),
            'score': float(results['final_score'])
        }

    except Exception as e:
        print(f"Error in quality checking: {e}")
        return False

# To check Not Safe For Work (NSFW) content
nsfw_model_path = "openai/clip-vit-base-patch32"
nsfw_model = CLIPModel.from_pretrained(nsfw_model_path)
nsfw_processor = CLIPProcessor.from_pretrained(nsfw_model_path)


def check_nsfw(image_bytes):
    '''Evaluate an image to check if it's NSFW (Not Safe For Work).'''
    try:
        # Open and convert image bytes to RGB format for processing
        with Image.open(BytesIO(image_bytes)).convert("RGB") as img:

            # Prepare input data for the NSFW classifier
            inputs = nsfw_processor(
                text=[
                    "gory, wound, bleeding, bloodshed",
                    "nudity",
                    "friendship, romantic, love, photography, family, selfie, enjoy, peoples, headshot, party, happiness, studying, exercise, fun, couple, sleeping, food, pizza, animal, eating, drinking, restaurant, water, sports, playing, fighting, lifestyle, bike, car, stunt, athletes, balance beam, artist, bed, room, house",
                    "animals, birds, insects, mammals, reptiles, amphibians, safe, normal, clothes, house, city, text, historical, nature, mountains, red, interesting, informative, art, cat, dog, vegitables, fruits, flowers, trees, plants, sky, clouds, sun, moon, stars, desert, forest, jungle",
                    "blood art, pain, hospital, fight, injection, red color, laboratory, light, fire design, shirt, dangerous, traffic, car, bike",
                ],
                
                images=img,
                return_tensors="pt",
                padding=True
            )

            # Run inference with no gradient computation (optimized)
            with torch.no_grad():
                outputs = nsfw_model(**inputs)

            # Calculate probabilities of NSFW and Safe classes
            logits_per_image = outputs.logits_per_image
            probs = logits_per_image.softmax(dim=1)
            print(probs)
            # print("NSFW Probability",probs)
            nsfw_prob_1 = probs[0][0].item()
            nsfw_prob_2 = probs[0][1].item()
            print(nsfw_prob_1, nsfw_prob_2)
            # Classify as "True" if the probability exceeds a threshold, otherwise "False"
            if nsfw_prob_1 > 0.85:
                return True, "Bloodshed", nsfw_prob_1
            elif nsfw_prob_2 > 0.95:
                return True, "Nudity or Pornography", nsfw_prob_2
            elif nsfw_prob_1 + nsfw_prob_2 > 0.98:
                return True, "Bloodshed and Nudity", nsfw_prob_1 + nsfw_prob_2
            else:
                return False, "Normal", 1 - (nsfw_prob_1 + nsfw_prob_2)
    except Exception as e:
        # Log any errors during NSFW check processing
        print(f"Error processing NSFW check: {e}")
        return "Error", None