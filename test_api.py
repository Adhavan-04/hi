import requests
import base64
import json
import numpy as np
import soundfile as sf
import io

def create_test_audio():
    """Create a synthetic test audio file"""
    # Generate a simple sine wave as test audio
    sample_rate = 22050
    duration = 2  # seconds
    frequency = 440  # Hz (A note)
    
    # Generate sine wave
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio_data = np.sin(2 * np.pi * frequency * t)
    
    # Add some random noise to make it more realistic
    audio_data += np.random.normal(0, 0.1, audio_data.shape)
    
    # Normalize
    audio_data = audio_data / np.max(np.abs(audio_data))
    
    # Convert to bytes
    buffer = io.BytesIO()
    sf.write(buffer, audio_data, sample_rate, format='WAV')
    buffer.seek(0)
    
    return buffer.read()

def test_api():
    """Test the API endpoint"""
    # API configuration
    API_URL = "http://localhost:5000/detect"
    API_KEY = "hackathon_api_key_2025"
    
    # Create test audio
    print("Creating test audio...")
    audio_bytes = create_test_audio()
    
    # Encode to base64
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    
    # Prepare request
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "audio": audio_base64
    }
    
    # Send request
    print(f"Sending request to {API_URL}...")
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            print("\n✅ API test successful!")
        else:
            print("\n❌ API test failed!")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

def test_health():
    """Test the health endpoint"""
    API_URL = "http://localhost:5000/health"
    
    print("Testing health endpoint...")
    try:
        response = requests.get(API_URL)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("=" * 50)
    print("AI Voice Detection API - Test Script")
    print("=" * 50)
    
    print("\n1. Testing health endpoint...")
    test_health()
    
    print("\n2. Testing detection endpoint...")
    test_api()
