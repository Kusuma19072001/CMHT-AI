#!/usr/bin/env python3
"""
Test script for Supabase feedback functionality
"""

from feedback_manager import feedback_manager
import json
from datetime import datetime

def test_supabase_connection():
    """Test basic Supabase connection"""
    print("🔍 Testing Supabase connection...")
    
    if feedback_manager.supabase:
        print("✅ Supabase client initialized successfully")
        return True
    else:
        print("❌ Failed to initialize Supabase client")
        return False

def test_feedback_operations():
    """Test feedback CRUD operations"""
    print("\n🔍 Testing feedback operations...")
    
    # Test data
    test_feedback = {
        "type": "test",
        "message": "This is a test feedback message",
        "name": "Test User",
        "email": "test@example.com",
        "rating": "5"
    }
    
    # Test 1: Store feedback
    print("📝 Testing feedback storage...")
    result = feedback_manager.store_feedback(test_feedback)
    
    if result["success"]:
        print(f"✅ Feedback stored successfully with ID: {result.get('id')}")
        feedback_id = result.get('id')
        
        # Test 2: Retrieve feedback
        print("📖 Testing feedback retrieval...")
        retrieve_result = feedback_manager.get_all_feedback(limit=5)
        
        if retrieve_result["success"]:
            print(f"✅ Retrieved {retrieve_result.get('count', 0)} feedback records")
            
            # Test 3: Get feedback stats
            print("📊 Testing feedback statistics...")
            stats_result = feedback_manager.get_feedback_stats()
            
            if stats_result["success"]:
                stats = stats_result.get("stats", {})
                print(f"✅ Total feedback: {stats.get('total_feedback', 0)}")
                print(f"✅ Feedback types: {stats.get('types_count', 0)}")
                print(f"✅ Type breakdown: {json.dumps(stats.get('by_type', {}), indent=2)}")
            else:
                print(f"❌ Failed to get stats: {stats_result.get('message')}")
        else:
            print(f"❌ Failed to retrieve feedback: {retrieve_result.get('message')}")
        
        # Test 4: Update feedback
        print("✏️ Testing feedback update...")
        update_data = {"message": "This is an updated test feedback message"}
        update_result = feedback_manager.update_feedback(feedback_id, update_data)
        
        if update_result["success"]:
            print("✅ Feedback updated successfully")
        else:
            print(f"❌ Failed to update feedback: {update_result.get('message')}")
        
        # Test 5: Delete test feedback
        print("🗑️ Testing feedback deletion...")
        delete_result = feedback_manager.delete_feedback(feedback_id)
        
        if delete_result["success"]:
            print("✅ Test feedback deleted successfully")
        else:
            print(f"❌ Failed to delete feedback: {delete_result.get('message')}")
        
        return True
    else:
        print(f"❌ Failed to store feedback: {result.get('message')}")
        return False

def test_feedback_by_type():
    """Test retrieving feedback by type"""
    print("\n🔍 Testing feedback retrieval by type...")
    
    # First, add some test feedback of different types
    test_feedbacks = [
        {"type": "general", "message": "General test feedback 1"},
        {"type": "technical", "message": "Technical test feedback 1"},
        {"type": "general", "message": "General test feedback 2"},
        {"type": "suggestion", "message": "Suggestion test feedback 1"}
    ]
    
    stored_ids = []
    
    for feedback in test_feedbacks:
        result = feedback_manager.store_feedback(feedback)
        if result["success"]:
            stored_ids.append(result.get('id'))
            print(f"✅ Stored {feedback['type']} feedback")
        else:
            print(f"❌ Failed to store {feedback['type']} feedback")
    
    if stored_ids:
        # Test retrieval by type
        print("\n📖 Testing retrieval by type...")
        
        for feedback_type in ["general", "technical", "suggestion"]:
            result = feedback_manager.get_feedback_by_type(feedback_type)
            if result["success"]:
                count = result.get("count", 0)
                print(f"✅ Found {count} {feedback_type} feedback records")
            else:
                print(f"❌ Failed to get {feedback_type} feedback: {result.get('message')}")
        
        # Clean up test data
        print("\n🧹 Cleaning up test data...")
        for feedback_id in stored_ids:
            delete_result = feedback_manager.delete_feedback(feedback_id)
            if delete_result["success"]:
                print(f"✅ Deleted feedback {feedback_id}")
            else:
                print(f"❌ Failed to delete feedback {feedback_id}")
        
        return True
    else:
        print("❌ No test feedback was stored, skipping type retrieval test")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Supabase feedback system tests...\n")
    
    # Test 1: Connection
    if not test_supabase_connection():
        print("\n❌ Connection test failed. Exiting.")
        return
    
    # Test 2: Basic operations
    if not test_feedback_operations():
        print("\n❌ Basic operations test failed.")
    
    # Test 3: Type-based retrieval
    if not test_feedback_by_type():
        print("\n❌ Type-based retrieval test failed.")
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    main() 