#!/usr/bin/env python3
"""
Test script to simulate the feedback form submission
"""

import requests
import json

def test_form_submission():
    """Test the feedback form submission with different data"""
    
    base_url = "http://localhost:8080"
    
    print("🧪 Testing Feedback Form Submission...")
    
    # Test 1: Submit feedback like the web form would
    print("\n1️⃣ Testing web form style submission...")
    
    # This simulates what the HTML form sends
    form_data = {
        "type": "general",
        "message": "This is my real feedback from the web form",
        "name": "Real User",
        "email": "realuser@example.com",
        "rating": "5"
    }
    
    try:
        response = requests.post(
            f"{base_url}/feedback",
            json=form_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("   ✅ Form feedback submitted successfully!")
                print(f"   Feedback ID: {result.get('feedback_id')}")
            else:
                print(f"   ❌ Form submission failed: {result.get('message')}")
        else:
            print(f"   ❌ HTTP error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error submitting form feedback: {str(e)}")
    
    # Test 2: Check current feedback count
    print("\n2️⃣ Checking current feedback count...")
    try:
        response = requests.get(f"{base_url}/feedback")
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                count = result.get("count", 0)
                print(f"   📊 Total feedback records: {count}")
                
                if count > 0:
                    print("   📝 Recent feedback:")
                    for feedback in result.get("data", [])[:5]:
                        print(f"      ID {feedback.get('id')}: {feedback.get('type')} - {feedback.get('message')[:50]}...")
            else:
                print(f"   ❌ Failed to get feedback: {result.get('message')}")
        else:
            print(f"   ❌ HTTP error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error getting feedback: {str(e)}")
    
    # Test 3: Check Supabase stats
    print("\n3️⃣ Checking Supabase statistics...")
    try:
        response = requests.get(f"{base_url}/feedback/stats")
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                stats = result.get("stats", {})
                print(f"   📊 Total feedback: {stats.get('total_feedback', 0)}")
                print(f"   📊 Types: {stats.get('types_count', 0)}")
                print(f"   📊 Type breakdown: {json.dumps(stats.get('by_type', {}), indent=2)}")
            else:
                print(f"   ❌ Failed to get stats: {result.get('message')}")
        else:
            print(f"   ❌ HTTP error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error getting stats: {str(e)}")

if __name__ == "__main__":
    test_form_submission() 