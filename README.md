AI Resume Intelligence Platform:
An AI-powered Resume Analysis and Hiring Prediction system that simulates the behavior of modern Applicant Tracking Systems (ATS). The platform evaluates resume–job alignment using NLP-based feature engineering and predicts hiring likelihood using a trained machine learning model.

Overview:
The AI Resume Intelligence Platform is designed to demonstrate end-to-end machine learning deployment in a production-style web application.
The system:
Parses resumes (PDF/Text format)
Extracts structured alignment signals
Computes ATS-style match metrics
Identifies missing skills
Predicts hiring probability using Logistic Regression
Implements secure authentication
Tracks user scores via leaderboard
Is deployed on Streamlit Cloud
The project emphasizes modular design, inference stability, and production reliability.

System Architecture:
User Input (Resume + Job Description)
            ↓
Streamlit UI (app.py)
            ↓
NLP Engine (nlp_engine.py)
            ↓
Feature Engineering
            ↓
ML Engine (ml_engine.py)
            ↓
Hiring Probability Prediction
            ↓
SQLite Database (database.py)

Core Components
1. app.py: 
Main Streamlit application responsible for:
User authentication (Sign Up / Login)
Resume upload and processing
Job description input
ATS scoring visualization
Hiring probability prediction
Leaderboard display

2. nlp_engine.py: 
Handles text processing and feature extraction:
Resume parsing
Job description normalization
Skill matching
Experience and education alignment scoring
Missing skill detection
Feature dictionary generation for ML inference

3. ml_engine.py:
Responsible for:
Loading trained model (hiring_model.pkl)
Validating feature dimensions before inference
Safe probability prediction
Exception-safe fallback handling
Includes validation using model.n_features_in_ to prevent runtime crashes caused by feature mismatches.

4. database.py:
Implements:
SQLite-based storage
SHA-256 password hashing
Username normalization
User score tracking

5. train_model.py:
Used for:
Structured feature engineering
Logistic Regression model training
Model serialization using joblib

Machine Learning Model:
Model: Logistic Regression
Library: Scikit-learn
Input Features:
Resume–job match score
Skill match percentage
Experience alignment score
Education alignment 

Production Safeguards:
Feature count validation before prediction
Exception-safe inference
Fallback return values to prevent application failure

Key Features:
Resume PDF parsing
ATS-style scoring
Skill gap identification
Hiring probability prediction
Secure authentication system
Leaderboard functionality
Cloud deployment

Installation:
Clone the repository:
git clone https://github.com/eshmitasaha2004-cpu/AI-Resume-Intelligence-System
cd ai-resume-intelligence-platform

Install dependencies:
pip install -r requirements.txt

Run locally:
streamlit run app.py

Model Training:
To retrain the hiring prediction model:
python train_model.py

This generates:
hiring_model.pkl
Ensure feature order consistency between training and inference.

Deployment:
The application is deployed using Streamlit Cloud.
Deployment considerations:
Avoid hardcoded file paths
Validate model feature dimensions
Implement safe model loading
Normalize authentication inputs
Handle inference exceptions gracefully

Engineering Highlights:
Modular architecture separating UI, NLP, ML, and database logic
Structured feature engineering from unstructured resume text
Production-safe ML inference validation
Secure credential handling
Cloud-ready deployment design

Future Enhancements:
Transformer-based semantic similarity scoring
GPT-powered resume improvement suggestions
REST API implementation using FastAPI
Docker containerization
PostgreSQL integration
Model versioning and monitoring

Author:

Eshmita Saha
B.Tech Student
Interested in Backend Systems, NLP, and ML Deployment
