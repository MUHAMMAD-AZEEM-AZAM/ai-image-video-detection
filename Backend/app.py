from flask import Flask, jsonify, request
import os
from flask_cors import CORS
from werkzeug.exceptions import RequestEntityTooLarge
from process_video import extract_frames_from_video
from utils import image_quality, check_nsfw, is_ai_generated

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.errorhandler(RequestEntityTooLarge)
def handle_large_file(error):
    return jsonify({'error': f'File size exceeds the maximum limit = {error}'}), 413

@app.route('/predict', methods=['POST'])
def check_duplication():
    try:
        # Get uploaded file from the request
        file = request.files['file']
        file_extension = os.path.splitext(file.filename)[1].lower()  # Extract the file extension
        file_bytes = file.read()  # Read the raw file bytes
        
        file_type = file.content_type
        
        # Log file information for debugging
        print("Received content type:", file_type)
        print("Received file extension:", file_extension)
        print("File size:", len(file_bytes))
        print(file_type)
        
        # Determine file size limit based on type and extension
        if file_extension in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
            max_size = 20*1024*1024  # 10 MB for images
        elif file_extension in ['.mp4', '.mov', '.mkv', '.avi', '.flv', '.webm', '.m4v', '.3gp', '.mpeg', '.ts']:
            max_size = 1000*1024*1024  # 30 MB for videos
        else:
            return jsonify({'error': 'Unsupported file type'}), 400

        # Check if the uploaded file exceeds the maximum allowed size
        if len(file_bytes) > max_size:
            return jsonify({'error': f'File size exceeds the limit for {file_extension}'}), 413
        
        # Image processing section
        if 'image' in file_type:
            image_quality_results = image_quality(file_bytes)
            print(image_quality_results)
            
            nsfw_status = check_nsfw(file_bytes)
            print(nsfw_status)
    
            # Check if image is AI Generated
            is_ai_results = is_ai_generated(file_bytes)
            print(is_ai_results)
            # keywords = get_keywords(file_bytes)
            
            return jsonify({
                "quality_results": image_quality_results,
                "nsfw_status": {
                    "status": nsfw_status[0],
                    "reason": nsfw_status[1],
                    "score": nsfw_status[2],
                },
                # "keywords": keywords,
                "AIvsHuman": is_ai_results
            }), 200

        elif 'video' in file_type:
            # Extract frames from video and check each frame for NSFW content
            video_frames = extract_frames_from_video(file_bytes)
            
            nsfw_detected = False
            nsfw_scores = []
            nsfw_reasons = []
            ai_vs_human_results = []
            ai_vs_human_scores = []
            image_quality_scores = []
        
            try:
                for frame in video_frames["frames"]:
                    frame_bytes = frame.get('bytes') if isinstance(frame, dict) and 'bytes' in frame else frame
                    
                    nsfw_status = check_nsfw(frame_bytes)
                    print(nsfw_status)
                    if nsfw_status[0] == True:
                        nsfw_detected = True
                    else:
                        nsfw_detected = False
                    nsfw_detected = nsfw_detected or nsfw_status[0] == "NSFW"
                    nsfw_scores.append(nsfw_status[2])
                    nsfw_reasons.append(nsfw_status[1])
                    
                    is_ai_result = is_ai_generated(frame_bytes)
                    print(is_ai_result)
                    ai_vs_human_results.append(is_ai_result['status'])
                    ai_vs_human_scores.append(is_ai_result['score'])
                    
                    image_quality_result = image_quality(frame_bytes)
                    print(image_quality_result)
                    image_quality_scores.append(image_quality_result['score'])
            except Exception as e:
                print(f"Error processing frames: {e}")
            try:
                # Determine final AI vs Human result
                ai_count = ai_vs_human_results.count('ai')
                human_count = ai_vs_human_results.count('human')
                final_ai_vs_human = 'ai' if ai_count > human_count else 'human'
                final_ai_vs_human_score = sum(ai_vs_human_scores) / len(ai_vs_human_scores)
        
                # Calculate average NSFW score
                final_nsfw_score = sum(nsfw_scores) / len(nsfw_scores)
                final_nsfw_reason = max(set(nsfw_reasons), key=nsfw_reasons.count)  # Most common reason
        
                # Calculate average image quality score
                final_image_quality_score = sum(image_quality_scores) / len(image_quality_scores)
                final_image_quality_status = (
                    "Low" if final_image_quality_score < 0.65 else
                    "Normal" if final_image_quality_score < 0.85 else
                    "High"
                )
        
                return jsonify({
                    "nsfw_status": {
                        "status": nsfw_detected,
                        "score": final_nsfw_score,
                        "reason": final_nsfw_reason
                    },
                    "AIvsHuman": {
                        "status": final_ai_vs_human,
                        "score": final_ai_vs_human_score,
                    },
                    "quality_results": {
                        "status": final_image_quality_status,
                        "score": final_image_quality_score
                    }
                }), 200
        
            except Exception as e:
                print(f"Error processing frames: {e}")
                return jsonify({'error': f'An error occurred: {e}'}), 500
    except Exception as e:
        # Return error response if any exception occurs
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)