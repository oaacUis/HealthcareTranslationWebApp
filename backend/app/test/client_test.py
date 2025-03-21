import requests
import json
import os

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


# Stt endpoint
audio_file_path = "input_voice_test.m4a"

if os.path.exists(audio_file_path):
    with open(audio_file_path, "rb") as file:

        files = {
            "audio_file": file
        }
        stt_input_data = {
            "use_openai": "false",  # Note: Booleans should be strings in form data
            "language_code": "es"
        }
        stt_response = requests.post(base_url + endpoints["stt"],
                                     data=stt_input_data,
                                     files=files,
                                     headers=headers)
        print(f"Status Code: {stt_response.status_code}")
        print(f"Response: {stt_response.json()}")
        print("="*50)
else:
    print(f"Error: {audio_file_path} does not exist.")

translate_input_data = {
    "text": stt_response.json().get("transcription"),
    "src_lang": "es",
    "dest_lang": "fr"
}

# Translate text
print("Checking the translation endpoint...")
translate_response = requests.post(base_url + endpoints["translate"],
                                   json=translate_input_data, headers=headers)

print(f"Status Code: {translate_response.status_code}")
print(f"Response: {translate_response.json()}")
print("="*50)

tts_input_data = {
    "input_text": translate_response.json().get("translated_text")
}

# Tts endpoint
print("Checking the text-to-speech endpoint...")
tts_response = requests.post(base_url + endpoints["tts"],
                             json=tts_input_data, headers=headers)
print(f"Status Code: {tts_response.status_code}")
if tts_response.status_code == 200:
    print("Response Successful")
print("="*50)
