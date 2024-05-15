#!/usr/bin/env python3
"""
My portfolio app
"""

import requests
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo


API_KEY = '35391bf0e26dc5c88a21b99255729f66' 
BASE_URL = 'http://api.openweathermap.org/geo/1.0/direct?q=Nairobi&limit=5&appid=35391bf0e26dc5c88a21b99255729f66'

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/farmer_weather'
mongo = PyMongo(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if 'username' not in data or 'location' not in data or 'crops' not in data:
        return jsonify({'error': 'Missing fields'}), 400
    existing_user = mongo.db.users.find_one({'username': data['username']})
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 409

    new_user = {
            'username': data['username'],
            'location': data['location'],
            'crops': data['crops']
            }

    mongo.db.users.insert_one(new_user)
    return jsonify({'message': 'User registered successfully'}), 201


app.route('/weather', methods=['GET'])
def get_weather():
    city_name = 'Nairobi'
    country_code = 'KE'

    url = f'{BASE_URL}?q={city_name},{country_code}&appid={API_KEY}&units=metric'

    response = requests.get(url)

    if response.status_code == 200:

        weather_data = response.json()

        location = weather_data['name']
        weather = weather_data['weather'][0]['description'].capitalize()
        temperature = weather_data['main']['temp']

        weather_data = {
                'location': location,
                'weather': weather,
                'temperature': f'{temperature}°C'
                }

        return jsonify(weather_data), 200
    else:
        return jsonify({'error': 'Failed to fetch weather data'}), response.status_code


    if __name__ == '__main__':
        app.run(debug=True)
