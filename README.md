# Spano AI - Nutrition Tracking Backend System

A comprehensive nutrition tracking backend system built with FastAPI that enables user registration, BMR calculation, meal logging, and nutrient intake tracking.

## Features

- **User Registration**: Register users with personal details for BMR calculation
- **BMR Calculation**: Calculate Basal Metabolic Rate using Harris-Benedict equation
- **Meal Logging**: Log meals with food items and timestamps
- **Nutrient Tracking**: Track calories, protein, carbs, and fiber intake
- **WhatsApp Webhook**: Simulate WhatsApp integration for meal logging
- **RESTful API**: Complete REST API with proper HTTP status codes
- **Data Storage**: In-memory storage with JSON-like structure

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- Pydantic

## Installation

1. **Clone or download the project files**

2. **Create a virtual environment** (recommended):
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the API**:
   - API Base URL: `http://localhost:8000`
   - Interactive API Docs: `http://localhost:8000/docs`
   - Alternative API Docs: `http://localhost:8000/redoc`

## API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Register User
**POST** `/register`

Register a new user with personal details for BMR calculation.

**Request Body:**
```json
{
  "name": "John Doe",
  "age": 30,
  "weight": 75.5,
  "height": 175.0,
  "gender": "male",
  "goal": "weight loss"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "User registered successfully",
  "user_id": "user_1_1234567890",
  "bmr": 1756.23
}
```

#### 2. Log Meals
**POST** `/log_meals`

Log a meal for a specific user.

**Request Body:**
```json
{
  "user": "user_1_1234567890",
  "meal": "lunch",
  "items": ["rice", "dal", "cucumber"]
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Meal logged successfully",
  "meal_id": "meal_1_1234567890",
  "nutrients": {
    "calories": 262,
    "protein": 10.2,
    "carbs": 51.6,
    "fiber": 8.4
  }
}
```

#### 3. Get User Meals
**GET** `/meals/{user}`

Get all meals for a specific user.

**Query Parameters:**
- `date` (optional): Filter by date in YYYY-MM-DD format

**Example:**
```
GET /meals/user_1_1234567890
GET /meals/user_1_1234567890?date=2025-01-15
```

**Response:**
```json
{
  "status": "success",
  "user": "user_1_1234567890",
  "meals": [
    {
      "id": "meal_1_1234567890",
      "user_id": "user_1_1234567890",
      "meal_type": "lunch",
      "food_items": ["rice", "dal", "cucumber"],
      "logged_at": "2025-01-15T12:30:00",
      "nutrients": {
        "calories": 262,
        "protein": 10.2,
        "carbs": 51.6,
        "fiber": 8.4
      }
    }
  ],
  "total_meals": 1
}
```

#### 4. Get User Status
**GET** `/status/{user}`

Get user's nutrient consumption summary.

**Example:**
```
GET /status/user_1_1234567890
```

**Response:**
```json
{
  "status": "success",
  "user": "user_1_1234567890",
  "user_info": {
    "name": "John Doe",
    "bmr": 1756.23
  },
  "consumed_nutrients": {
    "calories": 524,
    "protein": 20.4,
    "carbs": 103.2,
    "fiber": 16.8
  },
  "total_meals": 2
}
```

#### 5. WhatsApp Webhook
**POST** `/webhook`

Simulate WhatsApp webhook for meal logging.

**Request Body:**
```json
{
  "message": "log lunch: rice, dal, cucumber"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Meal logged via webhook successfully",
  "meal_id": "webhook_meal_1_1234567890",
  "meal_type": "lunch",
  "food_items": ["rice", "dal", "cucumber"],
  "nutrients": {
    "calories": 262,
    "protein": 10.2,
    "carbs": 51.6,
    "fiber": 8.4
  }
}
```

#### 6. Health Check
**GET** `/health`

Check system health and statistics.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-15T12:30:00",
  "users_count": 5,
  "meals_count": 12
}
```

## Food Database

The system includes a comprehensive food database with nutritional information for common foods:

- **Grains**: rice, bread, pasta
- **Proteins**: chicken, fish, beef, egg, dal
- **Dairy**: milk, yogurt, cheese
- **Vegetables**: cucumber, tomato, onion, carrot, spinach, potato
- **Fruits**: banana, apple
- **Others**: salad

Each food item includes:
- Calories
- Protein (grams)
- Carbohydrates (grams)
- Fiber (grams)

## BMR Calculation

The system uses the Harris-Benedict equation for BMR calculation:

**For Males:**
```
BMR = 88.362 + (13.397 × weight) + (4.799 × height) - (5.677 × age)
```

**For Females:**
```
BMR = 447.593 + (9.247 × weight) + (3.098 × height) - (4.33 × age)
```

## Usage Examples

### 1. Complete User Workflow

```bash
# 1. Register a user
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "age": 28,
    "weight": 65.0,
    "height": 165.0,
    "gender": "female",
    "goal": "maintain weight"
  }'

# 2. Log a meal
curl -X POST "http://localhost:8000/log_meals" \
  -H "Content-Type: application/json" \
  -d '{
    "user": "user_1_1234567890",
    "meal": "breakfast",
    "items": ["bread", "egg", "milk"]
  }'

# 3. Check user status
curl -X GET "http://localhost:8000/status/user_1_1234567890"

# 4. Get meals for today
curl -X GET "http://localhost:8000/meals/user_1_1234567890?date=2025-01-15"
```

### 2. WhatsApp Webhook Simulation

```bash
# Simulate WhatsApp message
curl -X POST "http://localhost:8000/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "log dinner: chicken, rice, salad"
  }'
```

## Error Handling

The API provides comprehensive error handling with appropriate HTTP status codes:

- **200**: Success (GET requests)
- **201**: Created (POST requests)
- **400**: Bad Request (validation errors)
- **404**: Not Found (user/resource not found)
- **500**: Internal Server Error

### Common Error Responses

```json
{
  "detail": "User not found"
}
```

```json
{
  "detail": "Invalid meal type. Must be breakfast, lunch, or dinner"
}
```

```json
{
  "detail": "Invalid message format. Expected: 'log [meal_type]: [food_items]'"
}
```

## Testing

### Manual Testing with curl

```bash
# Test user registration
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "age": 25,
    "weight": 70.0,
    "height": 170.0,
    "gender": "male",
    "goal": "test"
  }'

# Test meal logging
curl -X POST "http://localhost:8000/log_meals" \
  -H "Content-Type: application/json" \
  -d '{
    "user": "user_1_1234567890",
    "meal": "lunch",
    "items": ["rice", "chicken", "salad"]
  }'

# Test webhook
curl -X POST "http://localhost:8000/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "log breakfast: bread, milk, banana"
  }'
```

### Testing with Interactive API Documentation

1. Start the server: `python main.py`
2. Open browser: `http://localhost:8000/docs`
3. Use the interactive Swagger UI to test all endpoints

## Data Models

### User Model
```json
{
  "id": "string",
  "name": "string",
  "age": "integer",
  "weight": "float",
  "height": "float",
  "gender": "string",
  "goal": "string",
  "bmr": "float",
  "created_at": "datetime"
}
```

### Meal Model
```json
{
  "id": "string",
  "user_id": "string",
  "meal_type": "string",
  "food_items": "array",
  "logged_at": "datetime",
  "nutrients": "object"
}
```

## System Architecture

- **Framework**: FastAPI
- **Language**: Python 3.8+
- **Data Storage**: In-memory (dictionary)
- **API Style**: RESTful
- **Data Format**: JSON
- **Validation**: Pydantic models

## Security Considerations

- Input validation using Pydantic models
- Proper error handling without exposing system details
- HTTP status codes for different error types
- Data sanitization for webhook messages

## Deployment

For development:
```bash
python main.py
```

For production:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Notes

- Data is stored in memory and will be lost on server restart
- The food database is static and includes common foods
- Webhook uses a default user for demonstration
- All timestamps are in ISO format
- BMR calculation uses the Harris-Benedict equation

## Contributing

This is a demonstration project for the Spano AI assignment. The system implements all required features:

- User registration with BMR calculation
- Meal logging functionality
- Nutrient tracking
- WhatsApp webhook simulation
- RESTful API design
- Comprehensive error handling
- Complete documentation

## License

This project is created for educational and demonstration purposes. 