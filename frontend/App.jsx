import { useState } from "react";
import { getAuthToken, transcribeAudio, translateText, textToSpeech } from "./services/api";
import LanguageSelector from "./components/LanguageSelector";
import TranscriptDisplay from "./components/TranscriptDisplay";
import SpeakButton from "./components/SpeakButton";

function App() {
    const [token, setToken] = useState(null);
    const [transcription, setTranscription] = useState("");
    const [translatedText, setTranslatedText] = useState("");
    const [audioBlob, setAudioBlob] = useState(null);
    const [sourceLang, setSourceLang] = useState("auto");
    const [targetLang, setTargetLang] = useState("en");

    // Obtener el token de autenticación
    const handleLogin = async () => {
        const credentials = { username: "test", password: "1234" }; // Ajustar con credenciales reales
        const userToken = await getAuthToken(credentials);
        setToken(userToken);
    };

    // Procesar transcripción de audio
    const handleTranscription = async (file) => {
        if (!token) return alert("Please log in first");
        const result = await transcribeAudio(file, token);
        setTranscription(result);
    };

    // Traducir el texto transcrito
    const handleTranslation = async () => {
        if (!transcription) return alert("No text to translate");
        const result = await translateText(transcription, sourceLang, targetLang, token);
        setTranslatedText(result);
    };

    // Convertir texto traducido en audio
    const handleTTS = async () => {
        if (!translatedText) return alert("No text to convert");
        const audio = await textToSpeech(translatedText, token);
        setAudioBlob(audio);
    };

    return (
        <div>
            <h1>Medical AI Translator</h1>
            <button onClick={handleLogin}>Login</button>

            <LanguageSelector
                sourceLang={sourceLang}
                targetLang={targetLang}
                setSourceLang={setSourceLang}
                setTargetLang={setTargetLang}
            />

            <input type="file" onChange={(e) => handleTranscription(e.target.files[0])} />
            <button onClick={handleTranslation}>Translate</button>
            <button onClick={handleTTS}>Convert to Speech</button>

            <TranscriptDisplay transcription={transcription} translatedText={translatedText} />

            {audioBlob && <SpeakButton audioBlob={audioBlob} />}
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
