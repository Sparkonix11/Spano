#!/usr/bin/env python3
"""
Demo script for Spano AI Nutrition Tracking Backend
Shows a complete workflow example
"""

import requests
import json
from datetime import datetime

# API Base URL
BASE_URL = "http://localhost:8000"

def demo_complete_workflow():
    """Demonstrate a complete user workflow"""
    print("Spano AI Nutrition Tracking - Complete Workflow Demo")
    print("=" * 60)
    
    print("\n1. Registering a new user...")
    user_data = {
        "name": "Alice Johnson",
        "age": 28,
        "weight": 65.0,
        "height": 165.0,
        "gender": "female",
        "goal": "maintain weight"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register", json=user_data)
        if response.status_code == 201:
            result = response.json()
            user_id = result["user_id"]
            bmr = result["bmr"]
            print(f"User registered successfully!")
            print(f"   User ID: {user_id}")
            print(f"   BMR: {bmr} calories/day")
        else:
            print("User registration failed")
            return
    except Exception as e:
        print(f"Error: {e}")
        return
    
    print("\n2. Logging breakfast...")
    breakfast_data = {
        "user": user_id,
        "meal": "breakfast",
        "items": ["bread", "egg", "milk"]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/log_meals", json=breakfast_data)
        if response.status_code == 201:
            result = response.json()
            print(f"Breakfast logged successfully!")
            print(f"   Calories: {result['nutrients']['calories']}")
            print(f"   Protein: {result['nutrients']['protein']}g")
        else:
            print("Breakfast logging failed")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n3. Logging lunch...")
    lunch_data = {
        "user": user_id,
        "meal": "lunch",
        "items": ["rice", "chicken", "salad"]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/log_meals", json=lunch_data)
        if response.status_code == 201:
            result = response.json()
            print(f"Lunch logged successfully!")
            print(f"   Calories: {result['nutrients']['calories']}")
            print(f"   Protein: {result['nutrients']['protein']}g")
        else:
            print("Lunch logging failed")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n4. Logging dinner via WhatsApp webhook...")
    webhook_data = {
        "message": "log dinner: pasta, fish, tomato"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/webhook", json=webhook_data)
        if response.status_code == 200:
            result = response.json()
            print(f"Dinner logged via webhook!")
            print(f"   Calories: {result['nutrients']['calories']}")
            print(f"   Protein: {result['nutrients']['protein']}g")
        else:
            print("Webhook logging failed")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n5. Checking user status...")
    try:
        response = requests.get(f"{BASE_URL}/status/{user_id}")
        if response.status_code == 200:
            result = response.json()
            print(f"User status retrieved!")
            print(f"   Total Calories: {result['consumed_nutrients']['calories']}")
            print(f"   Total Protein: {result['consumed_nutrients']['protein']}g")
            print(f"   Total Meals: {result['total_meals']}")
            print(f"   BMR: {result['user_info']['bmr']} calories/day")
        else:
            print("Status check failed")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n6. Retrieving all meals...")
    try:
        response = requests.get(f"{BASE_URL}/meals/{user_id}")
        if response.status_code == 200:
            result = response.json()
            print(f"Retrieved {result['total_meals']} meals:")
            for meal in result['meals']:
                print(f"   - {meal['meal_type']}: {', '.join(meal['food_items'])}")
        else:
            print("Meal retrieval failed")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("\nTry the interactive API docs at: http://localhost:8000/docs")

def demo_bmr_calculation():
    """Demonstrate BMR calculation for different users"""
    print("\nBMR Calculation Demo")
    print("=" * 40)
    
    test_users = [
        {
            "name": "John (Male)",
            "age": 30,
            "weight": 75.0,
            "height": 175.0,
            "gender": "male",
            "goal": "weight loss"
        },
        {
            "name": "Sarah (Female)",
            "age": 25,
            "weight": 60.0,
            "height": 165.0,
            "gender": "female",
            "goal": "muscle gain"
        }
    ]
    
    for user_data in test_users:
        try:
            response = requests.post(f"{BASE_URL}/register", json=user_data)
            if response.status_code == 201:
                result = response.json()
                print(f"{user_data['name']}:")
                print(f"   Age: {user_data['age']}, Weight: {user_data['weight']}kg, Height: {user_data['height']}cm")
                print(f"   BMR: {result['bmr']} calories/day")
                print()
        except Exception as e:
            print(f"Error calculating BMR for {user_data['name']}: {e}")

def demo_food_database():
    """Demonstrate food database and nutrient calculation"""
    print("\nFood Database Demo")
    print("=" * 40)
    
    user_data = {
        "name": "Test User",
        "age": 25,
        "weight": 70.0,
        "height": 170.0,
        "gender": "male",
        "goal": "test"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register", json=user_data)
        if response.status_code == 201:
            user_id = response.json()["user_id"]
            
            food_combinations = [
                ["rice", "chicken", "salad"],
                ["bread", "egg", "milk"],
                ["pasta", "fish", "tomato"],
                ["banana", "yogurt", "honey"]
            ]
            
            for i, foods in enumerate(food_combinations, 1):
                meal_data = {
                    "user": user_id,
                    "meal": "test",
                    "items": foods
                }
                
                response = requests.post(f"{BASE_URL}/log_meals", json=meal_data)
                if response.status_code == 201:
                    result = response.json()
                    print(f"Combination {i}: {', '.join(foods)}")
                    print(f"   Calories: {result['nutrients']['calories']}")
                    print(f"   Protein: {result['nutrients']['protein']}g")
                    print(f"   Carbs: {result['nutrients']['carbs']}g")
                    print(f"   Fiber: {result['nutrients']['fiber']}g")
                    print()
        else:
            print("Failed to create test user")
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Main demo function"""
    print("Spano AI Nutrition Tracking Backend Demo")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("Server is not running. Please start the server first:")
            print("   python main.py")
            return
    except Exception:
        print("Server is not running. Please start the server first:")
        print("   python main.py")
        return
    
    demo_complete_workflow()
    demo_bmr_calculation()
    demo_food_database()
    
    print("\nDemo Summary:")
    print("User registration with BMR calculation")
    print("Meal logging with nutrient tracking")
    print("WhatsApp webhook integration")
    print("User status and meal retrieval")
    print("Comprehensive food database")
    print("Error handling and validation")

if __name__ == "__main__":
    main() 