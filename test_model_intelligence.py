#!/usr/bin/env python3
"""Test the Enhanced Model Intelligence System"""
import requests
import json
import sys
import os

BASE_URL = "http://localhost:3000"
TOKEN = None

def login():
    """Login and get authentication token"""
    print("\n🔐 Authenticating...")
    email = os.environ.get("OASIS_EMAIL", "admin@localhost")
    password = os.environ.get("OASIS_PASSWORD", "admin")
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auths/signin",
                                json={"email": email, "password": password})
        if response.status_code == 200:
            token = response.json().get("token")
            if token:
                print(f"✅ Logged in as {email}")
                return token
        print(f"❌ Login failed: HTTP {response.status_code}")
        print("💡 Create admin user at http://localhost:3000 or set OASIS_EMAIL/OASIS_PASSWORD")
        return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_capabilities():
    if not TOKEN:
        return False
    print("=" * 60)
    print("🧪 Testing Model Capabilities")
    print("=" * 60)
    try:
        r = requests.get(f"{BASE_URL}/api/v1/model-intelligence/capabilities",
                        headers={"Authorization": f"Bearer {TOKEN}"})
        if r.status_code == 200:
            data = r.json()
            print(f"✅ Found {len(data.get('capabilities', {}))} capability types")
            print(f"📊 {len(data.get('model_capabilities', {}))} model mappings")
            return True
        print(f"❌ Failed: HTTP {r.status_code}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_recommendation():
    if not TOKEN:
        return
    print("\n" + "=" * 60)
    print("🧪 Testing Model Recommendations")
    print("=" * 60)
    queries = ["Write Python code", "Explain AI", "Solve math: x²+5x+6=0"]
    for q in queries:
        try:
            r = requests.post(f"{BASE_URL}/api/v1/model-intelligence/recommend",
                            json={"query": q, "top_n": 3},
                            headers={"Authorization": f"Bearer {TOKEN}"})
            if r.status_code == 200:
                data = r.json()
                print(f"✅ '{q[:30]}...' → {data.get('detected_task')}: {len(data.get('recommended_models', []))} models")
            else:
                print(f"⚠️  HTTP {r.status_code}")
        except Exception as e:
            print(f"❌ {e}")

def test_metrics():
    if not TOKEN:
        return
    print("\n" + "=" * 60)
    print("🧪 Testing Metrics")
    print("=" * 60)
    try:
        r = requests.get(f"{BASE_URL}/api/v1/model-intelligence/metrics",
                        headers={"Authorization": f"Bearer {TOKEN}"})
        if r.status_code == 200:
            data = r.json()
            count = len(data.get('models', []))
            if count > 0:
                print(f"✅ Metrics for {count} models")
            else:
                print("⚠️  No metrics yet (expected on first run)")
        else:
            print(f"❌ HTTP {r.status_code}")
    except Exception as e:
        print(f"❌ {e}")

def main():
    global TOKEN
    print("\n" + "=" * 60)
    print("🚀 OASIS Model Intelligence - Test Suite")
    print("=" * 60)
    
    TOKEN = login()
    if not TOKEN:
        print("\n❌ Cannot proceed without authentication")
        print("💡 Create admin at http://localhost:3000 or set env vars")
        return 1
    
    passed = test_capabilities()
    test_recommendation()
    test_metrics()
    
    print("\n" + "=" * 60)
    print("✅ Tests complete! API is working." if passed else "⚠️  Some tests incomplete")
    print("📚 Docs: http://localhost:3000/docs#/model-intelligence")
    print("=" * 60 + "\n")
    return 0 if passed else 1

if __name__ == "__main__":
    sys.exit(main())
