#!/usr/bin/env python3
"""
NVIDIA Nemotron-Nano-9B-v2 Model Test
Tests the Nemotron model loader and API endpoints
"""

import requests
import json

BASE_URL = "http://localhost:3000/api/oasis"

def test_nemotron_status():
    """Check Nemotron model status"""
    print("🔍 Checking Nemotron status...")
    response = requests.get(f"{BASE_URL}/nemotron/status")
    result = response.json()
    print(f"Status: {json.dumps(result, indent=2)}")
    return result


def test_nemotron_load():
    """Load Nemotron model"""
    print("\n🚀 Loading NVIDIA Nemotron-Nano-9B-v2...")
    
    payload = {
        "model_name": "nvidia/NVIDIA-Nemotron-Nano-9B-v2",
        "dtype": "auto",
        "device_map": "auto"
    }
    
    response = requests.post(f"{BASE_URL}/nemotron/load", json=payload)
    result = response.json()
    print(f"Load Result: {json.dumps(result, indent=2)}")
    return result


def test_nemotron_generate():
    """Generate text with Nemotron"""
    print("\n💬 Generating text with Nemotron...")
    
    payload = {
        "prompt": "Explain quantum computing in simple terms:",
        "max_length": 256,
        "temperature": 0.7,
        "top_p": 0.9
    }
    
    response = requests.post(f"{BASE_URL}/nemotron/generate", json=payload)
    result = response.json()
    
    if result.get("status") == "success":
        print(f"✅ Generated text:")
        print(f"{result['generated_text']}")
    else:
        print(f"❌ Error: {result}")
    
    return result


def test_nemotron_embeddings():
    """Get embeddings from Nemotron"""
    print("\n🧮 Getting embeddings...")
    
    payload = {
        "text": "OASIS is an omniscient AI system with advanced capabilities."
    }
    
    response = requests.post(f"{BASE_URL}/nemotron/embeddings", json=payload)
    result = response.json()
    
    if result.get("status") == "success":
        print(f"✅ Embedding shape: {result['shape']}")
        print(f"First 5 values: {result['embeddings'][0][:5]}")
    else:
        print(f"❌ Error: {result}")
    
    return result


def test_nemotron_unload():
    """Unload Nemotron model"""
    print("\n🗑️  Unloading Nemotron model...")
    
    response = requests.post(f"{BASE_URL}/nemotron/unload")
    result = response.json()
    print(f"Unload Result: {json.dumps(result, indent=2)}")
    return result


def main():
    """Run all Nemotron tests"""
    print("=" * 60)
    print("NVIDIA Nemotron-Nano-9B-v2 Model Test Suite")
    print("=" * 60)
    
    try:
        # Check initial status
        status = test_nemotron_status()
        
        # Load model if not loaded
        if not status.get("loaded"):
            load_result = test_nemotron_load()
            if load_result.get("status") != "success":
                print("\n❌ Failed to load model. Exiting.")
                return
        
        # Test generation
        test_nemotron_generate()
        
        # Test embeddings
        test_nemotron_embeddings()
        
        # Check final status
        print("\n📊 Final status:")
        test_nemotron_status()
        
        print("\n✅ All tests complete!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to OASIS server")
        print("Make sure OASIS is running: ./launch_oasis.sh")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
