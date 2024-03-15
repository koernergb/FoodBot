from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

# Define sqlalchemy database model

Base = declarative_base()

class FoodPantry(Base):
    __tablename__ = 'food_pantries'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)
    phone = Column(String(20))
    distribution_dates = Column(Text)
    eligibility_requirements = Column(Text)
    language_support = Column(String(100))
    additional_notes = Column(Text)
    
    food_pantries = [
    {
        "name": "Food Pantry 1",
        "address": "123 Main St",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "opening_hours": [
            {"day": "Monday", "open": "09:00", "close": "17:00"},
            {"day": "Tuesday", "open": "09:00", "close": "17:00"},
            {"day": "Wednesday", "weeks": [2, 3], "open": "14:00", "close": "18:00"},
            {"day": "Saturday", "weeks": [3], "open": "10:00", "close": "15:00"},
        ]
    },
    # More food pantries...
]