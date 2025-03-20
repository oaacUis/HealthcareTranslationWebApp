const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

// Get auth token
export const getAuthToken = async (credentials) => {
    try {
        const formData = new URLSearchParams();
        formData.append("username", credentials.username);
        formData.append("password", credentials.password);

        const response = await fetch(`${API_BASE_URL}/auth/token`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: formData,
        });

        const data = await response.json();
        return data.access_token;
    } catch (error) {
        console.error("Auth Error:", error);
        return null;
    }
};

// (STT)
export const transcribeAudio = async (audioFile, token) => {
    try {
        console.log("Enviando audio a:", `${API_BASE_URL}/speech/speech-to-text`);
        console.log("Token:", token);
        console.log("Archivo:", audioFile)

        const formData = new FormData();
        formData.append("audio_file", audioFile);

        const response = await fetch(`${API_BASE_URL}/speech/speech-to-text`, {
            method: "POST",
            headers: { Authorization: `Bearer ${token}` },
            body: formData,
        });

        if (!response.ok) {
            throw new Error("Error during speech-to-text conversion");
        }

        const data = await response.json();
        return data.transcription;
    } catch (error) {
        console.error("STT Error:", error);
        return null;
    }
};

// (Translation)
export const translateText = async (text, sourceLang, targetLang, token) => {
    try {
        const response = await fetch(`${API_BASE_URL}/translate/translate`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
                text,
                source_lang: sourceLang,
                target_lang: targetLang,
            }),
        });

        if (!response.ok) {
            throw new Error("Error during text translation");
        }

        const data = await response.json();
        return data.translated_text;
    } catch (error) {
        console.error("Translation Error:", error);
        return null;
    }
};

// (TTS)
export const textToSpeech = async (text, token) => {
    try {
        const response = await fetch(`${API_BASE_URL}/speech/text-to-speech`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ input_text: text }),
        });

        if (!response.ok) {
            throw new Error("Error during text-to-speech conversion");
        }

        const audioBlob = await response.blob();  // Conv to a Blob
        const audioUrl = URL.createObjectURL(audioBlob); // Create URL temporal

        console.log("🎵 URL temporal creada:", audioUrl);
        return audioUrl;  // Return URL temporal
    } catch (error) {
        console.error("TTS Error:", error);
        return null;
    }
};

