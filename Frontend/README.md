# AI and Human Image/Video Classifier (NSFW Detection Included)

## Overview
This project is an advanced **AI-powered classifier** designed to detect whether an image or video is human-generated or AI-generated. It also includes functionality for **NSFW detection** and provides an **accuracy percentage** for images and videos.

This project aims to help identify and filter out AI-generated or inappropriate content by providing robust detection capabilities with confidence levels.

---

## Features
- **Human vs AI Classification**  
  Distinguishes between human-generated and AI-generated images and videos.
  
- **NSFW Detection**  
  Detects if the content (image/video) is NSFW (Not Safe for Work).
  
- **Accuracy Scores**  
  Provides confidence scores (in percentage) for each classification.

---

## Purpose
1. **AI Content Awareness**: Assist in identifying AI-generated images and videos for content authenticity verification.
2. **Content Moderation**: Aid platforms in filtering NSFW content.
3. **User Safety**: Enhance user experience by flagging inappropriate or AI-generated content.

---

## Workflow
1. **Data Input**  
   - Users upload images or videos for analysis.
   
2. **Preprocessing**  
   - Input content is preprocessed to ensure consistency for the classification models.

3. **Classification**  
   - **Model 1**: Detects whether the content is AI-generated or human-generated.  
   - **Model 2**: Analyzes content for NSFW classification.

4. **Output**  
   - Classification labels (e.g., "AI-Generated" or "Human-Generated").  
   - NSFW status (e.g., "Safe" or "NSFW").  
   - Accuracy percentage for each classification.

---

## Tech Stack
- **Backend**  
  - Python with Transformer, Pytorch for deep learning models.
  - Flask for API integration.
  
- **Frontend**  
  - React.js or Next.js for an interactive user interface.

- **Database**  
  - MongoDB or PostgreSQL for storing results and logs.

- **Deployment**  
  - Docker for containerization.
  - AWS/GCP for cloud hosting.

---

## Dataset
The project uses a combination of:
1. AI-generated datasets from **[Kaggle](https://www.kaggle.com/)** and other public repositories.
2. NSFW detection datasets (e.g., Open NSFW datasets).
3. Human-generated content datasets.

---

## Accuracy Metrics
- **Image Classification**: ~98% accuracy on the test set.  
- **Video Classification**: ~98% accuracy on the test set.  
- **NSFW Detection**: ~99% accuracy on the test set.

(Note: Accuracy values may vary depending on the dataset and testing conditions.)

---

## Installation
### Prerequisites
- Python 3.8+
- Node.js 14+
- Docker (Optional)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-human-classifier.git
   cd ai-human-classifier
