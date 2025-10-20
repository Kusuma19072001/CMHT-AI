#!/usr/bin/env python3
"""
Debug script to test the process_voice_query function step by step
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the function
from app import process_voice_query, search_faculty, preprocess_query

def debug_search():
    """Debug the process_voice_query function step by step"""
    
    test_query = "where is mahesh babu"
    print(f"Testing query: '{test_query}'")
    print("=" * 60)
    
    # Test preprocessing
    print("1. Testing preprocess_query:")
    processed = preprocess_query(test_query)
    print(f"   Original: '{test_query}'")
    print(f"   Processed: '{processed}'")
    print()
    
    # Test faculty indicators
    faculty_indicators = ["dr", "doctor", "professor", "prof", "faculty", "teacher", "instructor", "lecturer", "staff", "academic", "member", "where", "find", "located", "who", "what", "how", "meet", "looking", "trying", "need", "want", "would like", "office", "room"]
    print("2. Testing faculty indicators:")
    print(f"   Faculty indicators: {faculty_indicators}")
    print(f"   Contains faculty indicators: {any(indicator in processed for indicator in faculty_indicators)}")
    print()
    
    # Test the search_faculty function directly
    print("3. Testing search_faculty directly:")
    try:
        result = search_faculty(test_query)
        print(f"   Result: '{result}'")
    except Exception as e:
        print(f"   ERROR: {e}")
        import traceback
        traceback.print_exc()
    print()
    
    # Test the process_voice_query function (what the web app uses)
    print("4. Testing process_voice_query (web app function):")
    try:
        result2 = process_voice_query(test_query)
        print(f"   Result: '{result2}'")
    except Exception as e:
        print(f"   ERROR: {e}")
        import traceback
        traceback.print_exc()
    print()
    
    print("=" * 60)
    print("Debug completed!")

if __name__ == "__main__":
    debug_search() 