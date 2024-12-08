from io import BytesIO
from tempfile import NamedTemporaryFile
import os
import cv2
from PIL import Image

def extract_frames_from_video(
    video_bytes: bytes,
    base_frame_interval: int = 360
) -> dict:
    try:
        # Create a temporary video file to store the video bytes with supported video extensions
        video_extensions = ['.mp4', '.mov', '.mkv', '.avi', '.flv', '.webm', '.m4v', '.3gp', '.mpeg', '.ts']
        temp_video_file_path = None
        for ext in video_extensions:
            with NamedTemporaryFile(delete=False, suffix=ext) as temp_video_file:
                temp_video_file.write(video_bytes)
                temp_video_file_path = temp_video_file.name
                break
        if not temp_video_file_path:
            raise ValueError("Could not create a temporary video file.")

        video = cv2.VideoCapture(temp_video_file_path)  # Open video file
        fps = video.get(cv2.CAP_PROP_FPS)  # Frames per second
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))  # Total frame count
        video_duration = total_frames / fps if fps > 0 else 0  # Calculate video duration in seconds

        frames = []  # List to store extracted frames

        # Generate a list of frame indices to process
        frame_indices = range(0, total_frames, base_frame_interval)

        for frame_count in frame_indices:
            # Set the video position to the desired frame
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
            success, frame = video.read()
            if not success:
                continue  # Skip if the frame could not be read

            # Calculate the timestamp for the current frame
            frame_time = frame_count / fps if fps > 0 else 0  # Time in seconds
            print(f"Processing frame {frame_count} at {frame_time:.2f} seconds")

            # Convert frame to RGB and save as JPEG
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)

            buf = BytesIO()
            pil_image.save(buf, format='JPEG')
            frame_bytes = buf.getvalue()
            frames.append(frame_bytes)  # Append frame bytes to frames list

        video.release()  # Release video resource
        os.remove(temp_video_file_path)  # Delete temporary file

        return {"frames_extracted": len(frames), "frames": frames}

    except Exception as e:
        print(f"Error extracting frames from video: {e}")
        return {"error": str(e)}