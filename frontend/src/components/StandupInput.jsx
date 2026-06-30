import { useState, useEffect } from "react";

function StandupInput({
  onSend,
  isUpdateMode,
  initialText
}) {
  const [text, setText] = useState("");
  useEffect(() => {
    setText(initialText);
  }, [initialText]);

  const handleSubmit = async () => {
    if (!text.trim()) return;
    await onSend(text);
    };

  return (
    <div className="input-container">
      <textarea
        placeholder={
          isUpdateMode
            ? "Edit your standup..."
            : "Type your standup..."
        }
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button onClick={handleSubmit}>
        {isUpdateMode
          ? "Update Standup"
          : "Submit"}
      </button>
    </div>
  );
}

export default StandupInput;