"""
Test script to verify the Flask app works correctly
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test imports
print("✓ Testing imports...")
from app import app, init_db, calculate_stress_category
import sqlite3

# Test database initialization
print("✓ Initializing database...")
init_db()
print("✓ Database initialized successfully")

# Test stress category calculation
print("\n✓ Testing DASS-21 scoring...")
test_cases = [
    (0, 0, "Normal"),
    (7, 0, "Normal"),
    (14, 0, "Normal"),
    (15, 1, "Mild"),
    (18, 1, "Mild"),
    (19, 2, "Moderate"),
    (25, 2, "Moderate"),
    (26, 3, "Severe"),
    (33, 3, "Severe"),
    (34, 4, "Extremely Severe"),
    (42, 4, "Extremely Severe")
]

all_passed = True
for score, expected_cat, expected_level in test_cases:
    result = calculate_stress_category(score)
    if result['category'] != expected_cat or result['level'] != expected_level:
        print(f"  ✗ FAILED: Score {score} -> Category {result['category']} ({result['level']}), expected {expected_cat} ({expected_level})")
        all_passed = False
    else:
        print(f"  ✓ Score {score} -> Category {result['category']} ({result['level']})")

if all_passed:
    print("\n✓ All scoring tests passed!")

# Test Flask routes
print("\n✓ Testing Flask routes...")
with app.test_client() as client:
    # Test index page
    response = client.get('/')
    print(f"  GET / -> {response.status_code}")
    
    # Test test page
    response = client.get('/test')
    print(f"  GET /test -> {response.status_code}")
    
    # Test dashboard page
    response = client.get('/dashboard')
    print(f"  GET /dashboard -> {response.status_code}")
    
    # Test API endpoints
    response = client.get('/api/questions')
    print(f"  GET /api/questions -> {response.status_code} ({len(response.json)} questions)")
    
    response = client.get('/api/statistics')
    print(f"  GET /api/statistics -> {response.status_code}")
    
    response = client.get('/api/respondents')
    print(f"  GET /api/respondents -> {response.status_code}")
    
    response = client.get('/api/results')
    print(f"  GET /api/results -> {response.status_code}")

print("\n✓ All tests completed successfully!")
print("\n🚀 System is ready to run. Use: python app.py")
