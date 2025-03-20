import { useState } from "react";

const LanguageSelector = ({ onLanguageChange }) => {
  const [sourceLang, setSourceLang] = useState("auto");
  const [targetLang, setTargetLang] = useState("en");

  const languages = [
    { code: "auto", name: "Detect Language" },
    { code: "en", name: "English" },
    { code: "es", name: "Spanish" },
    { code: "fr", name: "French" },
    { code: "de", name: "German" },
    { code: "it", name: "Italian" },
    { code: "pt", name: "Portuguese" },
    { code: "zh", name: "Chinese" },
    { code: "ja", name: "Japanese" },
  ];

  const handleChange = (event, type) => {
    const value = event.target.value;
    if (type === "source") {
      setSourceLang(value);
      onLanguageChange(value, targetLang);
    } else {
      setTargetLang(value);
      onLanguageChange(sourceLang, value);
    }
  };

  return (
    <div className="p-4 border rounded-lg shadow-md">
      <label className="block font-semibold">Source Language:</label>
      <select
        value={sourceLang}
        onChange={(e) => handleChange(e, "source")}
        className="border p-2 w-full rounded mt-1"
      >
        {languages.map((lang) => (
          <option key={lang.code} value={lang.code}>
            {lang.name}
          </option>
        ))}
      </select>

      <label className="block font-semibold mt-4">Target Language:</label>
      <select
        value={targetLang}
        onChange={(e) => handleChange(e, "target")}
        className="border p-2 w-full rounded mt-1"
      >
        {languages.map((lang) => (
          <option key={lang.code} value={lang.code}>
            {lang.name}
          </option>
        ))}
      </select>
    </div>
  );
};

export default LanguageSelector;
