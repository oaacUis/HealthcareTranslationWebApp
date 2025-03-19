import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.routers.speech import router

from main import app  # Assuming your FastAPI app is defined in main.py

# Include the router in the app for testing
app.include_router(router)

client = TestClient(app)


class TestSpeechRouter(unittest.TestCase):
    @patch("app.routers.speech.process_input_audio")
    @patch("app.routers.speech.get_current_user")
    def test_speech_to_text_success(self, mock_get_current_user, mock_process_input_audio):
        mock_get_current_user.return_value = {"username": "test_user"}
        mock_process_input_audio.return_value = "This is a test transcription."

        # Simulate an audio file upload
        audio_content = b"fake audio content"
        files = {"audio_file": ("test_audio.mp3", audio_content, "audio/mpeg")}

        response = client.post("/speech/speech-to-text", files=files)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"transcription": "This is a test transcription."})

    @patch("app.routers.speech.process_input_audio")
    @patch("app.routers.speech.get_current_user")
    def test_speech_to_text_failure(self, mock_get_current_user, mock_process_input_audio):
        mock_get_current_user.return_value = {"username": "test_user"}
        mock_process_input_audio.side_effect = Exception("Processing error")

        # Simulate an audio file upload
        audio_content = b"fake audio content"
        files = {"audio_file": ("test_audio.mp3", audio_content, "audio/mpeg")}

        response = client.post("/speech/speech-to-text", files=files)

        self.assertEqual(response.status_code, 500)
        self.assertIn("Error during transcription", response.json()["detail"])

    @patch("app.routers.speech.process_output_audio")
    @patch("app.routers.speech.get_current_user")
    def test_text_to_speech_success(self, mock_get_current_user, mock_process_output_audio):
        mock_get_current_user.return_value = {"username": "test_user"}
        mock_process_output_audio.return_value = [b"fake audio chunk"]

        response = client.post("/speech/text-to-speech", json={"input_text": "Hello, world!"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "audio/mpeg")
        self.assertEqual(response.headers["content-disposition"], 'attachment; filename="output.mp3"')

    @patch("app.routers.speech.process_output_audio")
    @patch("app.routers.speech.get_current_user")
    def test_text_to_speech_failure(self, mock_get_current_user, mock_process_output_audio):
        mock_get_current_user.return_value = {"username": "test_user"}
        mock_process_output_audio.side_effect = Exception("Processing error")

        response = client.post("/speech/text-to-speech", json={"input_text": "Hello, world!"})

        self.assertEqual(response.status_code, 500)
        self.assertIn("Error during text-to-speech conversion", response.json()["detail"])


if __name__ == "__main__":
    unittest.main()
