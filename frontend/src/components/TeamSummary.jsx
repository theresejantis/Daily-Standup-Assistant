import { useState } from "react";
import { createSummary } from "../services/api";

function TeamSummary() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSummary = async () => {
    try {
      setLoading(true);

      const result = await createSummary();

      setSummary(result);
    } catch (error) {
      console.error("Summary Error:", error);
    } finally {
      setLoading(false);
    }
  };

  const cleanText = (text) => {
    return text
      .replace(/\*\*/g, "")
      .replace(/###/g, "")
      .replace(/---+/g, "")
      .replace(/===+/g, "");
  };

  return (
    <div className="summary-container">

      {!summary && (
        <button
          className="analysis-btn"
          onClick={handleSummary}
          disabled={loading}
        >
          {loading ? "Generating..." : "View Summary"}
        </button>
      )}

      {summary && (
        <div className="summary-panel">

          <button
            className="back-btn"
            onClick={() => setSummary(null)}
          >
            ← Back
          </button>

          <h3>Daily Team Summary</h3>

          {summary.message ? (
            <p>{summary.message}</p>
          ) : (
            <p style={{ whiteSpace: "pre-line" }}>
              {cleanText(summary.summary_text)}
            </p>
          )}

        </div>
      )}

    </div>
  );
}

export default TeamSummary;