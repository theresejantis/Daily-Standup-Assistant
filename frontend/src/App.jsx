import "./App.css";
import { useState, useEffect } from "react";

import UserSelection from "./components/UserSelection";
import StandupChat from "./components/StandupChat";
import StandupInput from "./components/StandupInput";
import ProgressAnalysis from "./components/ProgressAnalysis";
import TeamSummary from "./components/TeamSummary";

import {
  createStandup,
  updateStandup,
  getBlockers,
  getStandups,
  getEmployees
} from "./services/api";

function App() {

  const [selectedUser, setSelectedUser] = useState(null);

  const [messages, setMessages] = useState([]);

  const [submittedUsers, setSubmittedUsers] = useState([]);

  const [currentStandup, setCurrentStandup] = useState(null);

  const [updateMode, setUpdateMode] = useState(false);

  const loadStandups = async () => {

    try {

    const standups = await getStandups();

    const blockers = await getBlockers();

    const employees = await getEmployees();

    // Build chat messages
    const loadedMessages = standups.map((standup) => {

      const blocker = blockers.find(
        (b) => b.updated_id === standup.update_id
      );

      const employee = employees.find(
        (e) => e.employee_id === standup.employee_id
      );

      return {

        user: employee
          ? employee.employee_name
          : "Unknown",

        text: `
Yesterday:
${standup.yesterdays_work}

Today:
${standup.todays_work}

Blockers:
${blocker?.blocker_description || "None"}
`

      };

    });

    setMessages(loadedMessages);

    const submitted = standups
      .map((standup) => {

        const employee = employees.find(
          (e) => e.employee_id === standup.employee_id
        );

        return employee?.employee_name;

      })
      .filter(Boolean);

    setSubmittedUsers(submitted);

    
    if (selectedUser) {

      const employeeStandup = standups.find(
        (s) => s.employee_id === selectedUser.id
      );

      if (employeeStandup) {

        setCurrentStandup(employeeStandup);

        setUpdateMode(true);

      } else {

        setCurrentStandup(null);

        setUpdateMode(false);

      }

    }

  } catch (error) {

    console.error("Load Standups Error:", error);

  }

};

useEffect(() => {

  loadStandups();

}, []);

useEffect(() => {

  if (selectedUser) {

    loadStandups();

  }

}, [selectedUser]);

  const handleSend = async (text) => {

    try {

      let standup;

    if (updateMode) {

      standup = await updateStandup(
        currentStandup.update_id,
        selectedUser.id,
        text
        );

    } else {

      standup = await createStandup(
        selectedUser.id,
        text
      );

    }

      const blockers = await getBlockers();

      const blocker = blockers.find(
        (b) => b.updated_id === standup.update_id
      );

      const formattedMessage = `
Yesterday:
${standup.yesterdays_work}

Today:
${standup.todays_work}

Blockers:
${blocker?.blocker_description || "None"}
`;

      await loadStandups();

      if (!submittedUsers.includes(selectedUser.name)) {
        setSubmittedUsers([
          ...submittedUsers,
          selectedUser.name,
        ]);
      }

    } catch (error) {
      console.error("Standup Error:", error);
    }
  };

  if (!selectedUser) {
    return (
      <UserSelection
        onSelectUser={setSelectedUser}
      />
    );
  }

  return (
    <div className="workspace">

      <div className="sidebar">

        <h2>Employees</h2>

        <p>Therese</p>
        <p>John</p>
        <p>Alex</p>
        <p>Manager</p>

        <button
          className="back-btn"
          onClick={() => {
            setSelectedUser(null);
          }}
        >
          Change User
        </button>

      </div>

      <div className="main-content">

        <StandupChat
          messages={messages}
          selectedUser={selectedUser}
        />

        {selectedUser.name !== "Manager" && (

          <StandupInput
            onSend={handleSend}
            isUpdateMode={updateMode}
            initialText={
            currentStandup?.raw_msg || ""
            }
          />

        )}

        {selectedUser.name !== "Manager" && (

          <ProgressAnalysis
            employeeId={selectedUser.id}
            enabled={
              submittedUsers.includes(
                selectedUser.name
              )
            }
          />

        )}

        {selectedUser.name === "Manager" && (

          <TeamSummary />

        )}

      </div>

    </div>
  );
}

export default App;