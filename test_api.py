#!/usr/bin/env python3
"""
Test script for Spano AI Nutrition Tracking Backend
Demonstrates all API endpoints and functionality
"""

import requests
import json
import time
from datetime import datetime

# API Base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print("Health check passed\n")
        return True
    except Exception as e:
        print(f"Health check failed: {e}\n")
        return False

def test_user_registration():
    """Test user registration"""
    print("Testing User Registration...")
    
    user_data = {
        "name": "John Doe",
        "age": 30,
        "weight": 75.5,
        "height": 175.0,
        "gender": "male",
        "goal": "weight loss"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register", json=user_data)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if response.status_code == 201:
            print("User registration passed")
            return result.get("user_id")
        else:
            print("User registration failed")
            return None
    except Exception as e:
        print(f"User registration failed: {e}")
        return None

def test_meal_logging(user_id):
    """Test meal logging"""
    print(f"Testing Meal Logging for user: {user_id}")
    
    meals_to_log = [
        {
            "user": user_id,
            "meal": "breakfast",
            "items": ["bread", "egg", "milk"]
        },
        {
            "user": user_id,
            "meal": "lunch",
            "items": ["rice", "chicken", "salad"]
        },
        {
            "user": user_id,
            "meal": "dinner",
            "items": ["pasta", "fish", "tomato"]
        }
    ]
    
    for i, meal_data in enumerate(meals_to_log, 1):
        print(f"\n--- Meal {i}: {meal_data['meal']} ---")
        try:
            response = requests.post(f"{BASE_URL}/log_meals", json=meal_data)
            print(f"Status: {response.status_code}")
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            
            if response.status_code == 201:
                print(f"Meal {i} logged successfully")
            else:
                print(f"Meal {i} logging failed")
        except Exception as e:
            print(f"Meal {i} logging failed: {e}")

def test_get_meals(user_id):
    """Test getting user meals"""
    print(f"\nTesting Get User Meals for user: {user_id}")
    
    try:
        response = requests.get(f"{BASE_URL}/meals/{user_id}")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if response.status_code == 200:
            print("Get meals passed")
        else:
            print("Get meals failed")
    except Exception as e:
        print(f"Get meals failed: {e}")

def test_user_status(user_id):
    """Test getting user status"""
    print(f"\nTesting User Status for user: {user_id}")
    
    try:
        response = requests.get(f"{BASE_URL}/status/{user_id}")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if response.status_code == 200:
            print("User status passed")
        else:
            print("User status failed")
    except Exception as e:
        print(f"User status failed: {e}")

def test_webhook():
    """Test WhatsApp webhook"""
    print("\nTesting WhatsApp Webhook...")
    
    webhook_messages = [
        "log breakfast: bread, milk, banana",
        "log lunch: rice, dal, cucumber",
        "log dinner: chicken, pasta, salad"
    ]
    
    for i, message in enumerate(webhook_messages, 1):
        print(f"\n--- Webhook Message {i} ---")
        print(f"Message: {message}")
        
        webhook_data = {"message": message}
        
        try:
            response = requests.post(f"{BASE_URL}/webhook", json=webhook_data)
            print(f"Status: {response.status_code}")
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            
            if response.status_code == 200:
                print(f"Webhook {i} processed successfully")
            else:
                print(f"Webhook {i} processing failed")
        except Exception as e:
            print(f"Webhook {i} processing failed: {e}")

def test_error_handling():
    """Test error handling"""
    print("\nTesting Error Handling...")
    
    print("\n--- Invalid User Registration ---")
    invalid_user = {
        "name": "",
        "age": -5,
        "weight": 0,
        "height": 0,
        "gender": "invalid",
        "goal": ""
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register", json=invalid_user)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        print("Error handling for invalid registration passed")
    except Exception as e:
        print(f"Error handling test failed: {e}")
    
    print("\n--- Invalid Meal Logging ---")
    invalid_meal = {
        "user": "nonexistent_user",
        "meal": "invalid_meal",
        "items": []
    }
    
    try:
        response = requests.post(f"{BASE_URL}/log_meals", json=invalid_meal)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        print("Error handling for invalid meal logging passed")
    except Exception as e:
        print(f"Error handling test failed: {e}")
    
    print("\n--- Invalid Webhook Message ---")
    invalid_webhook = {"message": "invalid message format"}
    
    try:
        response = requests.post(f"{BASE_URL}/webhook", json=invalid_webhook)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        print("Error handling for invalid webhook passed")
    except Exception as e:
        print(f"Error handling test failed: {e}")

def main():
    """Main test function"""
    print("Starting Spano AI Nutrition Tracking Backend Tests")
    print("=" * 60)
    
    if not test_health_check():
        print("Server is not running. Please start the server first:")
        print("   python main.py")
        return
    
    user_id = test_user_registration()
    if not user_id:
        print("Cannot proceed without a valid user ID")
        return
    
    test_meal_logging(user_id)
    test_get_meals(user_id)
    test_user_status(user_id)
    test_webhook()
    test_error_handling()
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("\nYou can also test the API interactively at:")
    print("   http://localhost:8000/docs")

if __name__ == "__main__":
    main() 