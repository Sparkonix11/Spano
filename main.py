from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import json
import os
from enum import Enum

app = FastAPI(
    title="Spano AI - Nutrition Tracking Backend",
    description="A nutrition tracking backend system with user registration, BMR calculation, and meal logging",
    version="1.0.0"
)

users = {}
meals = {}
food_database = {
    "rice": {"calories": 130, "protein": 2.7, "carbs": 28, "fiber": 0.4},
    "dal": {"calories": 116, "protein": 6.8, "carbs": 20, "fiber": 7.5},
    "cucumber": {"calories": 16, "protein": 0.7, "carbs": 3.6, "fiber": 0.5},
    "chicken": {"calories": 165, "protein": 31, "carbs": 0, "fiber": 0},
    "bread": {"calories": 265, "protein": 9, "carbs": 49, "fiber": 2.7},
    "milk": {"calories": 42, "protein": 3.4, "carbs": 5, "fiber": 0},
    "egg": {"calories": 155, "protein": 13, "carbs": 1.1, "fiber": 0},
    "banana": {"calories": 89, "protein": 1.1, "carbs": 23, "fiber": 2.6},
    "apple": {"calories": 52, "protein": 0.3, "carbs": 14, "fiber": 2.4},
    "salad": {"calories": 20, "protein": 2, "carbs": 4, "fiber": 1.5},
    "pasta": {"calories": 131, "protein": 5, "carbs": 25, "fiber": 1.8},
    "fish": {"calories": 84, "protein": 18, "carbs": 0, "fiber": 0},
    "beef": {"calories": 250, "protein": 26, "carbs": 0, "fiber": 0},
    "potato": {"calories": 77, "protein": 2, "carbs": 17, "fiber": 2.2},
    "tomato": {"calories": 18, "protein": 0.9, "carbs": 3.9, "fiber": 1.2},
    "onion": {"calories": 40, "protein": 1.1, "carbs": 9.3, "fiber": 1.7},
    "carrot": {"calories": 41, "protein": 0.9, "carbs": 10, "fiber": 2.8},
    "spinach": {"calories": 23, "protein": 2.9, "carbs": 3.6, "fiber": 2.2},
    "yogurt": {"calories": 59, "protein": 10, "carbs": 3.6, "fiber": 0},
    "cheese": {"calories": 113, "protein": 7, "carbs": 0.4, "fiber": 0}
}

# Pydantic models
class Gender(str, Enum):
    male = "male"
    female = "female"

class UserRegistration(BaseModel):
    name: str = Field(..., min_length=1, description="User's full name")
    age: int = Field(..., gt=0, description="User's age in years")
    weight: float = Field(..., gt=0, description="User's weight in kg")
    height: float = Field(..., gt=0, description="User's height in cm")
    gender: Gender = Field(..., description="User's gender")
    goal: str = Field(..., min_length=1, description="User's fitness goal")

class MealLogging(BaseModel):
    user: str = Field(..., description="User ID")
    meal: str = Field(..., description="Meal type (breakfast/lunch/dinner)")
    items: List[str] = Field(..., min_items=1, description="List of food items")

class WebhookMessage(BaseModel):
    message: str = Field(..., description="WhatsApp message content")

# BMR Calculation Functions
def calculate_bmr(weight: float, height: float, age: int, gender: str) -> float:
    """
    Calculate Basal Metabolic Rate using Harris-Benedict equation
    
    Args:
        weight: Weight in kg
        height: Height in cm
        age: Age in years
        gender: 'male' or 'female'
    
    Returns:
        BMR value in calories
    """
    if gender.lower() == "male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender.lower() == "female":
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.33 * age)
    else:
        raise ValueError("Gender must be 'male' or 'female'")
    
    return round(bmr, 2)

def calculate_nutrients(food_items: List[str]) -> Dict[str, int]:
    """
    Calculate total nutrients for given food items
    
    Args:
        food_items: List of food item names
    
    Returns:
        Dictionary with total nutrients
    """
    total_nutrients = {"calories": 0, "protein": 0, "carbs": 0, "fiber": 0}
    
    for item in food_items:
        item_lower = item.lower().strip()
        if item_lower in food_database:
            nutrients = food_database[item_lower]
            total_nutrients["calories"] += nutrients["calories"]
            total_nutrients["protein"] += nutrients["protein"]
            total_nutrients["carbs"] += nutrients["carbs"]
            total_nutrients["fiber"] += nutrients["fiber"]
    
    return total_nutrients

# API Endpoints

@app.post("/register", status_code=201)
async def register_user(user_data: UserRegistration):
    """
    Register a new user with personal details
    
    Args:
        user_data: User registration data
    
    Returns:
        Success response with user ID
    """
    try:
        bmr = calculate_bmr(user_data.weight, user_data.height, user_data.age, user_data.gender)
        
        user_id = f"user_{len(users) + 1}_{int(datetime.now().timestamp())}"
        
        users[user_id] = {
            "id": user_id,
            "name": user_data.name,
            "age": user_data.age,
            "weight": user_data.weight,
            "height": user_data.height,
            "gender": user_data.gender,
            "goal": user_data.goal,
            "bmr": bmr,
            "created_at": datetime.now().isoformat()
        }
        
        return {
            "status": "success",
            "message": "User registered successfully",
            "user_id": user_id,
            "bmr": bmr
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")

@app.post("/log_meals", status_code=201)
async def log_meals(meal_data: MealLogging):
    """
    Log a meal for a user
    
    Args:
        meal_data: Meal logging data
    
    Returns:
        Success response with meal details
    """
    try:
        if meal_data.user not in users:
            raise HTTPException(status_code=404, detail="User not found")
        
        valid_meals = ["breakfast", "lunch", "dinner"]
        if meal_data.meal.lower() not in valid_meals:
            raise HTTPException(status_code=400, detail="Invalid meal type. Must be breakfast, lunch, or dinner")
        
        nutrients = calculate_nutrients(meal_data.items)
        
        meal_id = f"meal_{len(meals) + 1}_{int(datetime.now().timestamp())}"
        
        meals[meal_id] = {
            "id": meal_id,
            "user_id": meal_data.user,
            "meal_type": meal_data.meal.lower(),
            "food_items": meal_data.items,
            "logged_at": datetime.now().isoformat(),
            "nutrients": nutrients
        }
        
        return {
            "status": "success",
            "message": "Meal logged successfully",
            "meal_id": meal_id,
            "nutrients": nutrients
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Meal logging failed: {str(e)}")

@app.get("/meals/{user}")
async def get_user_meals(user: str, date: Optional[str] = None):
    """
    Get meals for a specific user, optionally filtered by date
    
    Args:
        user: User ID
        date: Optional date filter (YYYY-MM-DD format)
    
    Returns:
        List of user's meals
    """
    try:
        if user not in users:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_meals = [meal for meal in meals.values() if meal["user_id"] == user]
        
        if date:
            try:
                filter_date = datetime.strptime(date, "%Y-%m-%d").date()
                filtered_meals = []
                for meal in user_meals:
                    meal_date = datetime.fromisoformat(meal["logged_at"]).date()
                    if meal_date == filter_date:
                        filtered_meals.append(meal)
                user_meals = filtered_meals
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        
        return {
            "status": "success",
            "user": user,
            "meals": user_meals,
            "total_meals": len(user_meals)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve meals: {str(e)}")

@app.get("/status/{user}")
async def get_user_status(user: str):
    """
    Get user's nutrient consumption status
    
    Args:
        user: User ID
    
    Returns:
        User's nutrient consumption summary
    """
    try:
        if user not in users:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_meals = [meal for meal in meals.values() if meal["user_id"] == user]
        
        total_nutrients = {"calories": 0, "protein": 0, "carbs": 0, "fiber": 0}
        
        for meal in user_meals:
            nutrients = meal["nutrients"]
            total_nutrients["calories"] += nutrients["calories"]
            total_nutrients["protein"] += nutrients["protein"]
            total_nutrients["carbs"] += nutrients["carbs"]
            total_nutrients["fiber"] += nutrients["fiber"]
        
        user_bmr = users[user]["bmr"]
        
        return {
            "status": "success",
            "user": user,
            "user_info": {
                "name": users[user]["name"],
                "bmr": user_bmr
            },
            "consumed_nutrients": total_nutrients,
            "total_meals": len(user_meals)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user status: {str(e)}")

@app.post("/webhook")
async def webhook_handler(webhook_data: WebhookMessage):
    """
    Handle WhatsApp webhook messages for meal logging
    
    Args:
        webhook_data: Webhook message data
    
    Returns:
        Success response
    """
    try:
        message = webhook_data.message.strip()
        
        if not message.startswith("log "):
            raise HTTPException(status_code=400, detail="Invalid message format. Must start with 'log '")
        
        parts = message[4:].split(":", 1)
        if len(parts) != 2:
            raise HTTPException(status_code=400, detail="Invalid message format. Expected: 'log [meal_type]: [food_items]'")
        
        meal_type = parts[0].strip().lower()
        food_items_str = parts[1].strip()
        
        valid_meals = ["breakfast", "lunch", "dinner"]
        if meal_type not in valid_meals:
            raise HTTPException(status_code=400, detail="Invalid meal type. Must be breakfast, lunch, or dinner")
        
        food_items = [item.strip() for item in food_items_str.split(",")]
        food_items = [item for item in food_items if item]
        
        if not food_items:
            raise HTTPException(status_code=400, detail="No food items provided")
        
        default_user = "webhook_user"
        if default_user not in users:
            users[default_user] = {
                "id": default_user,
                "name": "Webhook User",
                "age": 25,
                "weight": 70.0,
                "height": 170.0,
                "gender": "male",
                "goal": "general",
                "bmr": calculate_bmr(70.0, 170.0, 25, "male"),
                "created_at": datetime.now().isoformat()
            }
        
        meal_id = f"webhook_meal_{len(meals) + 1}_{int(datetime.now().timestamp())}"
        nutrients = calculate_nutrients(food_items)
        
        meals[meal_id] = {
            "id": meal_id,
            "user_id": default_user,
            "meal_type": meal_type,
            "food_items": food_items,
            "logged_at": datetime.now().isoformat(),
            "nutrients": nutrients
        }
        
        return {
            "status": "success",
            "message": "Meal logged via webhook successfully",
            "meal_id": meal_id,
            "meal_type": meal_type,
            "food_items": food_items,
            "nutrients": nutrients
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook processing failed: {str(e)}")

@app.get("/")
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "Spano AI - Nutrition Tracking Backend",
        "version": "1.0.0",
        "endpoints": {
            "POST /register": "Register a new user",
            "POST /log_meals": "Log a meal for a user",
            "GET /meals/{user}": "Get user's meals (optional date filter)",
            "GET /status/{user}": "Get user's nutrient status",
            "POST /webhook": "WhatsApp webhook for meal logging"
        }
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "users_count": len(users),
        "meals_count": len(meals)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 