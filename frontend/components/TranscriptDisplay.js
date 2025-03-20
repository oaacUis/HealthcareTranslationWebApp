const TranscriptDisplay = ({ originalText, translatedText }) => {
    return (
      <div className="p-4 border rounded-lg shadow-md bg-white">
        <h2 className="text-lg font-semibold mb-2">Transcription</h2>
        <p className="p-2 border rounded bg-gray-100">
          {originalText || "Waiting for input..."}
        </p>
  
        <h2 className="text-lg font-semibold mt-4 mb-2">Translation</h2>
        <p className="p-2 border rounded bg-gray-100">
          {translatedText || "Translation will appear here..."}
        </p>
      </div>
    );
  };
  
  export default TranscriptDisplay;
  