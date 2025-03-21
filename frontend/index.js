import { useState } from "react";
import { useEffect } from "react";
import { useRouter } from "next/router";   
import { transcribeAudio, translateText, textToSpeech } from "./services/api";
import LanguageSelector from "./components/LanguageSelector";
import TranscriptDisplay from "./components/TranscriptDisplay";
import SpeakButton from "./components/SpeakButton";


export default function Home() {

    const router = useRouter();
    const [token, setToken] = useState(null);
    const [transcription, setTranscription] = useState("");
    const [translatedText, setTranslatedText] = useState("");
    const [audioBlob, setAudioBlob] = useState(null);
    const [sourceLang, setSourceLang] = useState("auto");
    const [targetLang, setTargetLang] = useState("en");

    useEffect(() => {
      const storedToken = localStorage.getItem("authToken");
      if (!storedToken) {
        router.push("/login"); // Redirect to login page
      } else {
          console.log("Token cargado:", storedToken);
          setToken(storedToken);
      }
    }, []);

    // Process Audio File
    const handleTranscription = async (file) => {
      console.log("📂 Archivo recibido:", file);
      if (!file) {
          alert("No file selected.");
          return;
      }
      if (!token) return alert("Please log in first");
      const result = await transcribeAudio(file, token);
      setTranscription(result);
    };

    // Translate Text
    const handleTranslation = async () => {
        if (!transcription) return alert("No text to translate");
        const result = await translateText(transcription, sourceLang, targetLang, token);
        setTranslatedText(result);
    };

    // Convert Text to Speech
    const handleTTS = async () => {
      if (!translatedText) return alert("No text to convert");
      
      const audioUrl = await textToSpeech(translatedText, token);
      if (!audioUrl) return alert("Error generating audio");
  
      console.log("🎵 URL final del audio:", audioUrl);
      setAudioBlob(audioUrl);
    };

    return (
      <div className="flex flex-col items-center justify-center h-screen bg-gray-100 p-4">
          <h1 className="text-3xl font-bold mb-4">Medical AI Translator</h1>

          <LanguageSelector
              onLanguageChange={(src, tgt) => {
                  setSourceLang(src);
                  setTargetLang(tgt);
              }}
          />

          <input
              key={Date.now()} // Forces re-render
              type="file"
              onChange={(e) => handleTranscription(e.target.files[0])}
              className="mb-2"
          />
          <button onClick={handleTranslation} className="bg-green-500 text-white px-4 py-2 rounded-md mx-2">
              Translate
          </button>
          <button onClick={handleTTS} className="bg-blue-500 text-white px-4 py-2 rounded-md">
              Convert to Speech
          </button>

          <TranscriptDisplay originalText={transcription} translatedText={translatedText} />

          {audioBlob && <SpeakButton audioUrl={audioBlob} />}
      </div>
  );
}