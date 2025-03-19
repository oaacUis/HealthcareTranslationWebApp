import requests
import json

# Base URL of the local app
base_url = "http://127.0.0.1:8000"

# Load the input data for the predict endpoint
with open('input_test.json') as f:
    input_data = json.load(f)
print(type(input_data))

# Authentication credentials
auth_data = {
    "username": "user",
    "password": "password"
}


def get_jwt_token(auth_url, auth_data):
    try:
        response = requests.post(auth_url, data=auth_data)
        print(response.json().get('access_token'))
        return response.json().get('access_token')
    except Exception as e:
        print(e)
        print("Could not get JWT token")
        return None


# Endpoints
endpoints = {
    "home": "/home",
    "translate": "/translate/translate",
    "stt": "/speech/speech-to-text",
    "tts": "/speech/text-to-speech"
}

# Test each endpoint
# Get JWT token
token = get_jwt_token(base_url + "/auth/token", auth_data)
headers = {'Authorization': f'Bearer {token}'}
print("headers:", headers), print()

print(), print("Checking the health of the api service...")
response_check = requests.get(base_url + endpoints["home"])
print(response_check.json())
print("="*50)


# Translate text
print("Checking the translation endpoint...")
translate_response = requests.post(base_url + endpoints["translate"],
                                   json=input_data, headers=headers)

print(f"Status Code: {translate_response.status_code}")
print(f"Response: {translate_response.json()}")
print("="*50)


# Stt endpoint
print("Checking the speech-to-text endpoint...")
audio_file = {"file": open("input_voice_test.mp3", "rb")}
stt_response = requests.post(base_url + endpoints["stt"],
                             files=audio_file, headers=headers)
print(f"Status Code: {stt_response.status_code}")
print(f"Response: {stt_response.json()}")
print("="*50)

# Tts endpoint
"""
print("Checking the text-to-speech endpoint...")
tts_response = requests.post(base_url + endpoints["tts"],
                             json=input_data, headers=headers)
print(f"Status Code: {tts_response.status_code}")
print(f"Response: {tts_response.json()}")
print("="*50)"""
