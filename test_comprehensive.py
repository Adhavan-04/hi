import requests
import base64
import json
import numpy as np
import soundfile as sf
import io
import time

API_KEY = "hackathon_api_key_2025"

def create_human_like_audio():
    """Create synthetic audio that mimics human speech patterns"""
    sample_rate = 22050
    duration = 3
    
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Create varied frequency pattern (like human speech)
    frequencies = [200, 250, 300, 280, 260]  # Varying pitch
    audio_data = np.zeros_like(t)
    
    segment_length = len(t) // len(frequencies)
    for i, freq in enumerate(frequencies):
        start = i * segment_length
        end = (i + 1) * segment_length if i < len(frequencies) - 1 else len(t)
        audio_data[start:end] = np.sin(2 * np.pi * freq * t[start:end])
    
    # Add natural variation and harmonics
    audio_data += 0.3 * np.sin(4 * np.pi * 220 * t)  # Harmonic
    audio_data += np.random.normal(0, 0.15, audio_data.shape)  # Natural noise
    
    # Add amplitude variation (breathing, emphasis)
    envelope = 1 + 0.3 * np.sin(2 * np.pi * 0.5 * t)
    audio_data *= envelope
    
    # Normalize
    audio_data = audio_data / np.max(np.abs(audio_data)) * 0.8
    
    buffer = io.BytesIO()
    sf.write(buffer, audio_data, sample_rate, format='WAV')
    buffer.seek(0)
    return buffer.read()

def create_ai_like_audio():
    """Create synthetic audio that mimics AI-generated speech"""
    sample_rate = 22050
    duration = 3
    
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Create consistent frequency pattern (like AI speech)
    frequency = 220  # Very consistent pitch
    audio_data = np.sin(2 * np.pi * frequency * t)
    
    # Add consistent harmonics
    audio_data += 0.4 * np.sin(4 * np.pi * frequency * t)
    audio_data += 0.2 * np.sin(6 * np.pi * frequency * t)
    
    # Add minimal noise (AI is cleaner)
    audio_data += np.random.normal(0, 0.05, audio_data.shape)
    
    # Very consistent amplitude
    audio_data = audio_data / np.max(np.abs(audio_data)) * 0.9
    
    buffer = io.BytesIO()
    sf.write(buffer, audio_data, sample_rate, format='WAV')
    buffer.seek(0)
    return buffer.read()

def test_endpoint(base_url, audio_bytes, test_name):
    """Test the API with given audio"""
    url = f"{base_url}/detect"
    
    # Encode to base64
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {"audio": audio_base64}
    
    print(f"\n{'='*60}")
    print(f"Test: {test_name}")
    print(f"{'='*60}")
    
    try:
        start_time = time.time()
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        elapsed_time = time.time() - start_time
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {elapsed_time:.2f} seconds")
        print(f"\nResponse Body:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Classification: {result['classification']}")
            print(f"✅ Confidence: {result['confidence']}")
            print(f"✅ Language: {result['language']}")
            return True
        else:
            print(f"\n❌ Test failed with status code {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"\n❌ Request timed out after 30 seconds")
        return False
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

def test_health(base_url):
    """Test health endpoint"""
    url = f"{base_url}/health"
    
    print(f"\n{'='*60}")
    print("Health Check")
    print(f"{'='*60}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("\n✅ Health check passed")
            return True
        else:
            print("\n❌ Health check failed")
            return False
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

def test_authentication(base_url):
    """Test API authentication"""
    url = f"{base_url}/detect"
    
    print(f"\n{'='*60}")
    print("Authentication Test (Invalid Key)")
    print(f"{'='*60}")
    
    audio_bytes = create_human_like_audio()
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    
    headers = {
        "Authorization": "invalid_key_12345",
        "Content-Type": "application/json"
    }
    
    payload = {"audio": audio_base64}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 401:
            print("\n✅ Authentication properly rejected invalid key")
            return True
        else:
            print("\n❌ Authentication test failed - should return 401")
            return False
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

def test_invalid_payload(base_url):
    """Test with invalid payload"""
    url = f"{base_url}/detect"
    
    print(f"\n{'='*60}")
    print("Invalid Payload Test")
    print(f"{'='*60}")
    
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {"invalid_field": "test"}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 400:
            print("\n✅ Properly handled invalid payload")
            return True
        else:
            print("\n❌ Invalid payload test failed - should return 400")
            return False
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

def main():
    """Main test function"""
    print("="*60)
    print("AI VOICE DETECTION API - COMPREHENSIVE TEST SUITE")
    print("="*60)
    
    # Get base URL
    base_url = input("\nEnter API base URL (default: http://localhost:5000): ").strip()
    if not base_url:
        base_url = "http://localhost:5000"
    
    print(f"\nTesting API at: {base_url}")
    
    results = []
    
    # Test 1: Health Check
    results.append(("Health Check", test_health(base_url)))
    
    # Test 2: Authentication
    results.append(("Authentication", test_authentication(base_url)))
    
    # Test 3: Invalid Payload
    results.append(("Invalid Payload", test_invalid_payload(base_url)))
    
    # Test 4: Human-like Audio
    human_audio = create_human_like_audio()
    results.append(("Human-like Audio", test_endpoint(base_url, human_audio, "Human-like Audio Detection")))
    
    # Test 5: AI-like Audio
    ai_audio = create_ai_like_audio()
    results.append(("AI-like Audio", test_endpoint(base_url, ai_audio, "AI-like Audio Detection")))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:30} {status}")
    
    print(f"\n{'='*60}")
    print(f"Total: {passed}/{total} tests passed")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    print(f"{'='*60}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Your API is ready for submission!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review and fix the issues.")

if __name__ == "__main__":
    main()
