import { useState } from "react";
import { createAnalysis } from "../services/api";

function ProgressAnalysis({ employeeId, enabled }) {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalysis = async () => {
    try {
      setLoading(true);

      const result = await createAnalysis(employeeId);

      setAnalysis(result);
    } catch (error) {
      console.error("Analysis Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="analysis-container">

      <button
        className="analysis-btn"
        disabled={!enabled || loading}
        onClick={handleAnalysis}
      >
        {loading ? "Generating..." : "View Analysis"}
      </button>

      {analysis && (
        <div className="analysis-panel">

          <h3>Progress Analysis</h3>

          <p>
            <strong>Previous Progress:</strong>{" "}
            {analysis.previous_progress}
          </p>

          <p>
            <strong>Current Progress:</strong>{" "}
            {analysis.current_progress}
          </p>

          <p>
            <strong>Work Status:</strong>{" "}
            {analysis.work_status}
          </p>

          <p>
            <strong>Jira Alignment:</strong>{" "}
            {analysis.jira_alignment}
          </p>

          <p>
            <strong>Delay Detected:</strong>{" "}
            {analysis.delay_detected}
          </p>

        </div>
      )}

    </div>
  );
}

export default ProgressAnalysis;