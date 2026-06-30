const BASE_URL = "http://127.0.0.1:8000";

export const createStandup = async (employeeId, rawMsg) => {
  const response = await fetch(`${BASE_URL}/standups/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      employee_id: employeeId,
      raw_msg: rawMsg,
    }),
  });

  return response.json();
};

export const createAnalysis = async (employeeId) => {
  const response = await fetch(
    `${BASE_URL}/progress-analysis/${employeeId}`,
    {
      method: "POST",
    }
  );

  return response.json();
};

export const getEmployees = async () => {
  const response = await fetch(`${BASE_URL}/employees/`);
  return response.json();
};

export const getBlockers = async () => {
  const response = await fetch(
    `${BASE_URL}/blockers/`
  );

  return response.json();
};

export const createSummary = async () => {
  const response = await fetch(
    `${BASE_URL}/team-summaries/`,
    {
      method: "POST",
    }
  );

  return response.json();
};

export const getSummary = async () => {
  const response = await fetch(
    `${BASE_URL}/team-summaries/`
  );

  return response.json();
};

export const getStandups = async () => {
  const response = await fetch(
    `${BASE_URL}/standups/`
  );

  return response.json();
};

export const updateStandup = async (
  updateId,
  employeeId,
  rawMsg
) => {
  const response = await fetch(
    `${BASE_URL}/standups/${updateId}`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        employee_id: employeeId,
        raw_msg: rawMsg,
      }),
    }
  );

  return response.json();
};

