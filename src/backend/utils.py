from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
from datetime import datetime, timedelta, time
from math import radians, sin, cos, sqrt, atan2
import json


def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    radius = 6371  # Radius of the Earth in kilometers
    distance = radius * c

    return distance


def calculate_distances(user_lat, user_lon, food_pantries):

  distances = {}

  for pantry in food_pantries:
    pantry_lat = pantry['latitude']
    pantry_lon = pantry['longitude']

    distance = calculate_distance(user_lat, user_lon, pantry_lat, pantry_lon)
    
    distances[pantry['name']] = distance

  return distances


def generate_distance_string(user_lat, user_lon, food_pantries):

  distances = calculate_distances(user_lat, user_lon, food_pantries)

  dist_string = ""
  for name, dist in distances.items():
    dist_string += f"{name}, {dist}\n"
  
  return dist_string


def print_pantries(food_pantries, user_lat, user_long):
    for pantry in food_pantries:
        print("Name: ", pantry["name"])
        print("Notes: ", pantry["notes"])
        print("Address: ", pantry["address"])
        lat = pantry["latitude"]
        long = pantry["longitude"]
        distance = calculate_distance(lat, long, user_lat, user_long)
        print("Distance from User: ", distance)
        print("Opening Hours: \n")
        for opening_hour in pantry["opening_hours"]:
            print("  Day: ", opening_hour["day"])
            if "weeks" in opening_hour:
                print("  Weeks: ", opening_hour["weeks"])
            print("  Open: ", opening_hour["open"])
            print("  Close: ", opening_hour["close"])
        print("---\n")

def generate_pantries_string(food_pantries, user_lat, user_long):
    info = ""
    for pantry in food_pantries:
        info += "Name: " + pantry["name"] + "\n"
        info += "Notes: " + pantry["notes"] + "\n"
        info += "Address: " + pantry["address"] + "\n"
        lat = pantry["latitude"]
        long = pantry["longitude"]
        distance = calculate_distance(lat, long, user_lat, user_long)
        info += "Distance from User: " + str(distance) + "\n"
        info += "Opening Hours: \n"
        for opening_hour in pantry["opening_hours"]:
            info += "  Day: " + opening_hour["day"] + "\n"
            if "weeks" in opening_hour:
                info += "  Weeks: " + str(opening_hour["weeks"]) + "\n"
            info += "  Open: " + str(opening_hour["open"]) + "\n"
            info += "  Close: " + str(opening_hour["close"]) + "\n"
        info += "---\n"
    return info



def list_next_openings(current_time, food_pantries, num_openings=10):
    result = []
    increment = timedelta(days=1)  # Increment one day at a time
    
    # Keep looking ahead until we find num_openings or reach an arbitrary lookahead limit (e.g., 60 days)
    for day_offset in range(60): 
        next_date = current_time.date() + day_offset * increment
        next_week = (next_date.day - 1) // 7 + 1
        next_day_name = next_date.strftime("%A")
        
        for pantry in food_pantries:
            for hours in pantry["opening_hours"]:
                # Check for matching day
                if hours["day"] == next_day_name:
                    day_has_weeks = "weeks" in hours
                    # If 'weeks' is specified, check if current week matches
                    if not day_has_weeks or next_week in hours["weeks"]:
                        open_time_str = hours.get("open", "00:00")
                        close_time_str = hours.get("close", "23:59")
                        open_datetime = datetime.combine(next_date, datetime.strptime(open_time_str, "%H:%M").time())
                        close_datetime = datetime.combine(next_date, datetime.strptime(close_time_str, "%H:%M").time())
                        # Check if this is an opening after the current time
                        if open_datetime > current_time:
                            result.append({
                                "pantry": pantry["name"],
                                "open_time": open_datetime,
                                "close_time": close_datetime,
                            })
                            # Sort and limit to the next num_openings
                            result = sorted(result, key=lambda x: x["open_time"])[:num_openings]
                            if len(result) == num_openings:
                                return result
    return result


def generate_user_context(user_latitude, user_longitude, current_time, food_pantries):

    distances_str = generate_distance_string(user_latitude, user_longitude, food_pantries)
    next_openings_str = list_next_openings(current_time, food_pantries, 10)
    pantries_str = generate_pantries_string(food_pantries, user_latitude, user_longitude)

    context = f"""
        Here is a list of the distances between the user and the food pantries:
        {distances_str}
        Here is a list of the next 10 open pantry distributions  
        {next_openings_str}  
        And here is a json file listing all the food pantries' information
        {pantries_str}"""

    return context
