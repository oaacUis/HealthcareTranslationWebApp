import { useState } from "react";
import TranscriptDisplay from "./components/TranscriptDisplay";
import LanguageSelector from "./components/LanguageSelector";
import SpeakButton from "./components/SpeakButton";
import api from "./services/api";
import "./styles/global.css";

function App() {
  const [selectedLanguage, setSelectedLanguage] = useState("en");
  const [transcription, setTranscription] = useState("");
  const [translatedText, setTranslatedText] = useState("");
  const [audioUrl, setAudioUrl] = useState(null);

  const handleLanguageChange = (language) => {
    setSelectedLanguage(language);
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("audio_file", file);

    try {
      const response = await api.post("/speech-to-text", formData);
      setTranscription(response.data.transcription);
    } catch (error) {
      console.error("Error transcribing audio:", error);
    }
  };

  const handleTranslate = async () => {
    try {
      const response = await api.post("/translate", {
        text: transcription,
        source_lang: "auto",
        target_lang: selectedLanguage,
      });
      setTranslatedText(response.data.translated_text);
    } catch (error) {
      console.error("Error translating text:", error);
    }
  };

  const handleTextToSpeech = async () => {
    try {
      const response = await api.post("/text-to-speech", {
        input_text: translatedText,
      });
      setAudioUrl(response.data.audio_url);
    } catch (error) {
      console.error("Error generating speech:", error);
    }
  };

  return (
    <div className="app-container">
      <h1>Healthcare Translation App</h1>
      
      <div className="upload-section">
        <input type="file" accept="audio/*" onChange={handleFileUpload} />
      </div>

      <TranscriptDisplay text={transcription} />

      <LanguageSelector
        selectedLanguage={selectedLanguage}
        onLanguageChange={handleLanguageChange}
      />

      <button onClick={handleTranslate} disabled={!transcription}>
        Translate
      </button>

      <TranscriptDisplay text={translatedText} />

      <button onClick={handleTextToSpeech} disabled={!translatedText}>
        Convert to Speech
      </button>

      {audioUrl && <SpeakButton audioUrl={audioUrl} />}
    </div>
  );
}

export default App;

// next.config.js
//module.exports = {
//  reactStrictMode: true,
//  env: {
//    NEXT_PUBLIC_API_BASE_URL: "http://localhost:8000" // Cambiar en producción
//  }
//};
