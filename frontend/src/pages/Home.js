import { useState } from "react";
import LanguageSelector from "../components/LanguageSelector";
import TranscriptDisplay from "../components/TranscriptDisplay";
import SpeakButton from "../components/SpeakButton";
import api from "../services/api";

const Home = () => {
  const [transcription, setTranscription] = useState("");
  const [translatedText, setTranslatedText] = useState("");
  const [audioUrl, setAudioUrl] = useState("");
  const [sourceLang, setSourceLang] = useState("es");
  const [targetLang, setTargetLang] = useState("en");
  const [loading, setLoading] = useState(false);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("audio_file", file);

    setLoading(true);
    try {
      // Speech-to-Text (STT)
      const sttResponse = await api.post("/speech-to-text", formData);
      setTranscription(sttResponse.data.transcription);

      // Translation
      const translateResponse = await api.post("/translate", {
        text: sttResponse.data.transcription,
        source_lang: sourceLang,
        target_lang: targetLang,
      });
      setTranslatedText(translateResponse.data.translated_text);

      // Text-to-Speech (TTS)
      const ttsResponse = await api.post("/text-to-speech", {
        input_text: translateResponse.data.translated_text,
      });
      setAudioUrl(ttsResponse.data.audio_url);
    } catch (error) {
      console.error("Error processing audio:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-6">
      <h1 className="text-2xl font-bold mb-4">Healthcare Translation Web App</h1>

      <div className="mb-4">
        <LanguageSelector
          sourceLang={sourceLang}
          targetLang={targetLang}
          onSourceLangChange={setSourceLang}
          onTargetLangChange={setTargetLang}
        />
      </div>

      <input
        type="file"
        accept="audio/*"
        onChange={handleFileUpload}
        className="mb-4 p-2 border rounded"
      />

      {loading && <p>Processing...</p>}

      <TranscriptDisplay transcription={transcription} translatedText={translatedText} />

      <SpeakButton audioUrl={audioUrl} />
    </div>
  );
};

export default Home;
