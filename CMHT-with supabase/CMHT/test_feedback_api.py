#!/usr/bin/env python3
"""
Test script to check if the feedback API is working
"""

import requests
import json

def test_feedback_api():
    """Test the feedback API endpoints"""
    
    base_url = "http://localhost:8080"
    
    print("🧪 Testing Feedback API...")
    
    # Test 1: Check if the feedback form page loads
    print("\n1️⃣ Testing feedback form page...")
    try:
        response = requests.get(f"{base_url}/feedback-form")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Feedback form page loads successfully")
        else:
            print(f"   ❌ Failed to load feedback form: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error accessing feedback form: {str(e)}")
    
    # Test 2: Submit test feedback
    print("\n2️⃣ Testing feedback submission...")
    test_feedback = {
        "type": "test",
        "message": "This is a test feedback message",
        "name": "Test User",
        "email": "test@example.com",
        "rating": "5"
    }
    
    try:
        response = requests.post(
            f"{base_url}/feedback",
            json=test_feedback,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("   ✅ Feedback submitted successfully!")
                print(f"   Feedback ID: {result.get('feedback_id')}")
            else:
                print(f"   ❌ Feedback submission failed: {result.get('message')}")
        else:
            print(f"   ❌ HTTP error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error submitting feedback: {str(e)}")
    
    # Test 3: Check if feedback was stored
    print("\n3️⃣ Testing feedback retrieval...")
    try:
        response = requests.get(f"{base_url}/feedback")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                count = result.get("count", 0)
                print(f"   ✅ Retrieved {count} feedback records")
                if count > 0:
                    print("   📝 Recent feedback:")
                    for feedback in result.get("data", [])[:3]:
                        print(f"      - {feedback.get('type')}: {feedback.get('message')[:50]}...")
                else:
                    print("   📝 No feedback records found")
            else:
                print(f"   ❌ Failed to retrieve feedback: {result.get('message')}")
        else:
            print(f"   ❌ HTTP error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error retrieving feedback: {str(e)}")
    
    # Test 4: Check feedback statistics
    print("\n4️⃣ Testing feedback statistics...")
    try:
        response = requests.get(f"{base_url}/feedback/stats")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                stats = result.get("stats", {})
                total = stats.get("total_feedback", 0)
                print(f"   ✅ Total feedback: {total}")
                print(f"   📊 Types: {stats.get('types_count', 0)}")
            else:
                print(f"   ❌ Failed to get stats: {result.get('message')}")
        else:
            print(f"   ❌ HTTP error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error getting stats: {str(e)}")

if __name__ == "__main__":
    test_feedback_api() 