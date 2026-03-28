#!/usr/bin/env python3
"""
API Key Verification Script
Tests all configured API keys to ensure they're working correctly
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_linkedin_token():
    """Test LinkedIn API token"""
    print_header("🔷 Testing LinkedIn API Token")
    
    token = os.getenv("LINKEDIN_TOKEN")
    if not token:
        print("❌ LINKEDIN_TOKEN not found in .env")
        return False
    
    print(f"Token found: {token[:20]}..." if len(token) > 20 else f"Token found: {token}")
    
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get('https://api.linkedin.com/v2/userinfo', headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            person_id = data.get('sub')
            email = data.get('email')
            print(f"✅ LinkedIn Token is VALID")
            print(f"   Person ID: {person_id}")
            print(f"   Email: {email}")
            return True
        elif response.status_code == 401:
            print(f"❌ LinkedIn Token is INVALID (401 Unauthorized)")
            print(f"   Error: {response.text}")
            return False
        else:
            print(f"⚠️  LinkedIn API returned {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    
    except requests.exceptions.Timeout:
        print("❌ Request timed out - LinkedIn API not responding")
        return False
    except Exception as e:
        print(f"❌ Error testing LinkedIn token: {str(e)}")
        return False

def test_stability_ai_key():
    """Test Stability AI API key"""
    print_header("🎨 Testing Stability AI API Key")
    
    key = os.getenv("STABILITY_API_KEY")
    if not key:
        print("❌ STABILITY_API_KEY not found in .env")
        return False
    
    print(f"Key found: {key[:20]}..." if len(key) > 20 else f"Key found: {key}")
    
    try:
        # Test with a minimal request (no actual generation)
        headers = {
            "authorization": f"Bearer {key}",
            "accept": "application/json"
        }
        
        response = requests.get('https://api.stability.ai/v1/engines/list', headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Stability AI Key is VALID")
            data = response.json()
            print(f"   Available engines: {len(data)}")
            return True
        elif response.status_code == 401:
            print(f"❌ Stability AI Key is INVALID (401 Unauthorized)")
            return False
        elif response.status_code == 402:
            print(f"⚠️  Stability AI Key has no credits (402 Payment Required)")
            print(f"   But key is valid! Get credits at: https://platform.stability.ai/account/credits")
            return True  # Key is valid, just no credits
        else:
            print(f"⚠️  Stability AI API returned {response.status_code}")
            return False
    
    except requests.exceptions.Timeout:
        print("❌ Request timed out - Stability AI API not responding")
        return False
    except Exception as e:
        print(f"❌ Error testing Stability AI key: {str(e)}")
        return False

def test_groq_api_key():
    """Test Groq API key"""
    print_header("🚀 Testing Groq API Key")
    
    key = os.getenv("GROQ_API_KEY")
    if not key:
        print("⏭️  GROQ_API_KEY not found in .env (optional)")
        return None
    
    print(f"Key found: {key[:20]}..." if len(key) > 20 else f"Key found: {key}")
    
    try:
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        
        response = requests.get('https://api.groq.com/openai/v1/models', headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Groq API Key is VALID")
            data = response.json()
            print(f"   Available models: {len(data.get('data', []))}")
            return True
        elif response.status_code == 401:
            print(f"❌ Groq API Key is INVALID (401 Unauthorized)")
            return False
        else:
            print(f"⚠️  Groq API returned {response.status_code}")
            return False
    
    except Exception as e:
        print(f"⚠️  Error testing Groq key: {str(e)}")
        return None

def test_gemini_api_key():
    """Test Gemini API key"""
    print_header("🤖 Testing Gemini API Key")
    
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        print("⏭️  GEMINI_API_KEY not found in .env (optional)")
        return None
    
    print(f"Key found: {key[:20]}..." if len(key) > 20 else f"Key found: {key}")
    
    try:
        response = requests.get(
            f'https://generativelanguage.googleapis.com/v1beta/models?key={key}',
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"✅ Gemini API Key is VALID")
            data = response.json()
            print(f"   Available models: {len(data.get('models', []))}")
            return True
        elif response.status_code == 400:
            print(f"❌ Gemini API Key is INVALID (400 Bad Request)")
            return False
        elif response.status_code == 403:
            print(f"❌ Gemini API Key is INVALID (403 Forbidden)")
            return False
        else:
            print(f"⚠️  Gemini API returned {response.status_code}")
            return False
    
    except Exception as e:
        print(f"⚠️  Error testing Gemini key: {str(e)}")
        return None

def test_replicate_api_key():
    """Test Replicate API key"""
    print_header("🔄 Testing Replicate API Key")
    
    key = os.getenv("REPLICATE_API_KEY")
    if not key:
        print("⏭️  REPLICATE_API_KEY not found in .env (optional)")
        return None
    
    print(f"Key found: {key[:20]}..." if len(key) > 20 else f"Key found: {key}")
    
    try:
        headers = {
            "Authorization": f"Token {key}",
            "Content-Type": "application/json"
        }
        
        response = requests.get('https://api.replicate.com/v1/account', headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Replicate API Key is VALID")
            data = response.json()
            print(f"   Account: {data.get('username', 'Unknown')}")
            return True
        elif response.status_code == 401:
            print(f"❌ Replicate API Key is INVALID (401 Unauthorized)")
            return False
        else:
            print(f"⚠️  Replicate API returned {response.status_code}")
            return False
    
    except Exception as e:
        print(f"⚠️  Error testing Replicate key: {str(e)}")
        return None

def test_huggingface_api_key():
    """Test HuggingFace API key"""
    print_header("🤗 Testing HuggingFace API Key")
    
    key = os.getenv("HUGGINGFACE_API_KEY")
    if not key:
        print("⏭️  HUGGINGFACE_API_KEY not found in .env (optional)")
        return None
    
    print(f"Key found: {key[:20]}..." if len(key) > 20 else f"Key found: {key}")
    
    try:
        headers = {
            "Authorization": f"Bearer {key}"
        }
        
        response = requests.get('https://huggingface.co/api/whoami', headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ HuggingFace API Key is VALID")
            data = response.json()
            print(f"   Username: {data.get('name', 'Unknown')}")
            return True
        elif response.status_code == 401:
            print(f"❌ HuggingFace API Key is INVALID (401 Unauthorized)")
            return False
        else:
            print(f"⚠️  HuggingFace API returned {response.status_code}")
            return False
    
    except Exception as e:
        print(f"⚠️  Error testing HuggingFace key: {str(e)}")
        return None

def main():
    """Run all API key tests"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "API KEY VERIFICATION REPORT" + " "*16 + "║")
    print("║" + " "*14 + f"Testing {6} API Keys" + " "*31 + "║")
    print("╚" + "="*58 + "╝")
    
    results = {
        "Critical": {},
        "Optional": {}
    }
    
    # Critical API keys (required for main functionality)
    print("\n[CRITICAL APIs - Required for main.py]")
    results["Critical"]["LinkedIn"] = test_linkedin_token()
    results["Critical"]["Stability AI"] = test_stability_ai_key()
    
    # Optional API keys
    print("\n[OPTIONAL APIs - For extended functionality]")
    results["Optional"]["Groq"] = test_groq_api_key()
    results["Optional"]["Gemini"] = test_gemini_api_key()
    results["Optional"]["Replicate"] = test_replicate_api_key()
    results["Optional"]["HuggingFace"] = test_huggingface_api_key()
    
    # Summary
    print_header("📊 TEST SUMMARY")
    
    critical_pass = sum(1 for v in results["Critical"].values() if v is True)
    critical_total = len(results["Critical"])
    print(f"\n✅ Critical APIs: {critical_pass}/{critical_total} working")
    for api, status in results["Critical"].items():
        emoji = "✅" if status else "❌"
        print(f"   {emoji} {api}")
    
    optional_results = {k: v for k, v in results["Optional"].items() if v is not None}
    if optional_results:
        optional_pass = sum(1 for v in optional_results.values() if v is True)
        optional_total = len(optional_results)
        print(f"\n⚙️  Optional APIs: {optional_pass}/{optional_total} working")
        for api, status in results["Optional"].items():
            if status is not None:
                emoji = "✅" if status else "❌"
                print(f"   {emoji} {api}")
    
    # Overall status
    print("\n" + "="*60)
    if critical_pass == critical_total:
        print("🎉 ALL CRITICAL APIs ARE WORKING! Ready to use main.py")
    else:
        print("⚠️  SOME CRITICAL APIs ARE NOT WORKING - Check configuration")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
