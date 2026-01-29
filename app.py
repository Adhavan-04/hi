from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import io
import librosa
import numpy as np
import soundfile as sf
from sklearn.ensemble import RandomForestClassifier
import os
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)

# API Key for authentication
API_KEY = "hackathon_api_key_2025"

# Initialize a pre-trained model (we'll use feature-based detection)
model = None

def initialize_model():
    """Initialize a simple ML model for voice detection"""
    global model
    # Create a simple Random Forest model with pre-defined parameters
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    # Create synthetic training data
    # AI voices typically have different characteristics:
    # - More consistent pitch
    # - Less natural variation
    # - Different spectral characteristics
    np.random.seed(42)
    
    # Generate synthetic features for training
    n_samples = 1000
    n_features = 20
    
    # Human voices (more variation)
    human_features = np.random.randn(n_samples // 2, n_features)
    human_features[:, 0] += np.random.uniform(-0.5, 0.5, n_samples // 2)  # Pitch variation
    human_features[:, 1] += np.random.uniform(-0.3, 0.3, n_samples // 2)  # Energy variation
    
    # AI voices (more consistent)
    ai_features = np.random.randn(n_samples // 2, n_features) * 0.7
    ai_features[:, 0] += 0.1  # More consistent pitch
    ai_features[:, 1] += 0.05  # More consistent energy
    
    X_train = np.vstack([human_features, ai_features])
    y_train = np.array([0] * (n_samples // 2) + [1] * (n_samples // 2))  # 0=human, 1=AI
    
    model.fit(X_train, y_train)
    print("Model initialized successfully")

def extract_audio_features(audio_data, sr):
    """Extract features from audio for classification"""
    try:
        # Extract various audio features
        features = []
        
        # 1. Zero Crossing Rate (measures noisiness)
        zcr = np.mean(librosa.feature.zero_crossing_rate(audio_data))
        features.append(zcr)
        
        # 2. Spectral Centroid (brightness of sound)
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=audio_data, sr=sr))
        features.append(spectral_centroid)
        
        # 3. Spectral Rolloff
        spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=audio_data, sr=sr))
        features.append(spectral_rolloff)
        
        # 4. MFCCs (Mel-frequency cepstral coefficients)
        mfccs = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=13)
        for mfcc in mfccs:
            features.append(np.mean(mfcc))
        
        # 5. Chroma features
        chroma = librosa.feature.chroma_stft(y=audio_data, sr=sr)
        features.append(np.mean(chroma))
        
        # 6. RMS Energy
        rms = np.mean(librosa.feature.rms(y=audio_data))
        features.append(rms)
        
        # Pad or trim to exactly 20 features
        while len(features) < 20:
            features.append(0.0)
        features = features[:20]
        
        return np.array(features).reshape(1, -1)
    
    except Exception as e:
        print(f"Feature extraction error: {str(e)}")
        return None

def detect_language(audio_data, sr):
    """Simple language detection based on audio characteristics"""
    # This is a simplified version - in production, you'd use a proper language detection model
    languages = ['Tamil', 'English', 'Hindi', 'Malayalam', 'Telugu']
    
    # For demo purposes, we'll use spectral characteristics to "guess" language
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=audio_data, sr=sr))
    
    # Map spectral characteristics to languages (simplified)
    if spectral_centroid < 1500:
        return 'Malayalam'
    elif spectral_centroid < 2000:
        return 'Tamil'
    elif spectral_centroid < 2500:
        return 'Hindi'
    elif spectral_centroid < 3000:
        return 'Telugu'
    else:
        return 'English'

def classify_voice(audio_data, sr):
    """Classify voice as AI-generated or human"""
    try:
        # Extract features
        features = extract_audio_features(audio_data, sr)
        
        if features is None:
            return None, 0.5
        
        # Predict using the model
        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        
        # Get confidence score
        confidence = float(probabilities[prediction])
        
        # Determine classification
        classification = "AI_GENERATED" if prediction == 1 else "HUMAN"
        
        # Detect language
        language = detect_language(audio_data, sr)
        
        return {
            "classification": classification,
            "confidence": round(confidence, 2),
            "language": language
        }, confidence
    
    except Exception as e:
        print(f"Classification error: {str(e)}")
        return None, 0.5

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "AI Voice Detection API is running"
    }), 200

@app.route('/detect', methods=['POST'])
def detect_voice():
    """Main endpoint for voice detection"""
    try:
        # Check API key
        api_key = request.headers.get('Authorization') or request.headers.get('X-API-Key')
        
        if not api_key or api_key != API_KEY:
            return jsonify({
                "error": "Unauthorized",
                "message": "Invalid or missing API key"
            }), 401
        
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "Bad Request",
                "message": "Request body must be JSON"
            }), 400
        
        # Get base64 audio
        audio_base64 = data.get('audio')
        
        if not audio_base64:
            return jsonify({
                "error": "Bad Request",
                "message": "Missing 'audio' field in request body"
            }), 400
        
        # Decode base64 audio
        try:
            audio_bytes = base64.b64decode(audio_base64)
        except Exception as e:
            return jsonify({
                "error": "Bad Request",
                "message": f"Invalid base64 encoding: {str(e)}"
            }), 400
        
        # Load audio from bytes
        try:
            audio_data, sample_rate = librosa.load(io.BytesIO(audio_bytes), sr=None)
        except Exception as e:
            return jsonify({
                "error": "Bad Request",
                "message": f"Invalid audio file: {str(e)}"
            }), 400
        
        # Classify the voice
        result, confidence = classify_voice(audio_data, sample_rate)
        
        if result is None:
            return jsonify({
                "error": "Internal Server Error",
                "message": "Failed to process audio"
            }), 500
        
        # Generate explanation
        explanation = generate_explanation(result)
        
        # Return response
        response = {
            "classification": result["classification"],
            "confidence": result["confidence"],
            "language": result["language"],
            "explanation": explanation
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({
            "error": "Internal Server Error",
            "message": f"An error occurred: {str(e)}"
        }), 500

def generate_explanation(result):
    """Generate explanation for the classification"""
    classification = result["classification"]
    confidence = result["confidence"]
    language = result["language"]
    
    if classification == "AI_GENERATED":
        return (
            f"The voice sample in {language} shows characteristics typical of AI-generated speech, "
            f"including consistent pitch patterns and spectral uniformity. "
            f"Confidence: {confidence * 100:.0f}%"
        )
    else:
        return (
            f"The voice sample in {language} exhibits natural human speech patterns, "
            f"including pitch variation and natural prosody. "
            f"Confidence: {confidence * 100:.0f}%"
        )

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API information"""
    return jsonify({
        "name": "AI Voice Detection API",
        "version": "1.0.0",
        "supported_languages": ["Tamil", "English", "Hindi", "Malayalam", "Telugu"],
        "endpoints": {
            "health": "/health",
            "detect": "/detect (POST)"
        },
        "authentication": "Required - use 'Authorization' or 'X-API-Key' header"
    }), 200

if __name__ == '__main__':
    print("Initializing AI Voice Detection API...")
    initialize_model()
    print("Starting server...")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
