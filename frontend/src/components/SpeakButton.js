import { useState } from "react";

const SpeakButton = ({ audioUrl }) => {
  console.log("🔊 Audio URL:", audioUrl);
  const [isPlaying, setIsPlaying] = useState(false);

  const handlePlay = () => {
      if (!audioUrl) return alert("Couldn't find audio URL");
      const audio = new Audio(audioUrl);
      setIsPlaying(true);
      audio.play();
      audio.onended = () => setIsPlaying(false);
  };

  return (
      <button
          onClick={handlePlay}
          disabled={!audioUrl || isPlaying}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg shadow-md hover:bg-blue-600 disabled:bg-gray-400"
      >
          {isPlaying ? "Playing..." : "Play Audio"}
      </button>
  );
};

export default SpeakButton;
