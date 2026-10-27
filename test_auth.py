#!/usr/bin/env python3
import requests
import json

# Test OASIS auth endpoint
try:
    # Test if server is responding
    response = requests.get('http://localhost:8080/auth', timeout=5)
    print(f"✅ Server responding: {response.status_code}")
    
    # Test signup endpoint
    signup_data = {
        "name": "dqikst",
        "email": "dqikst@gmail.com", 
        "password": "Havikz11"
    }
    
    signup_response = requests.post(
        'http://localhost:8080/api/v1/auths/signup',
        json=signup_data,
        timeout=10
    )
    
    print(f"📝 Signup attempt: {signup_response.status_code}")
    if signup_response.status_code == 200:
        print("✅ Account created successfully!")
        print(f"Response: {signup_response.json()}")
    else:
        print(f"❌ Signup failed: {signup_response.text}")
        
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to OASIS server")
except Exception as e:
    print(f"❌ Error: {e}")