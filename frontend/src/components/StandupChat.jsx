function StandupChat({ messages, selectedUser }) {
  return (
    <div className="chat-container">

      <h2>Daily Standup Channel</h2>

      <div className="bot-message">
        <strong>Standup Bot:</strong>

        <p>Yesterday's Work:</p>
        <p>Today's Work:</p>
        <p>Blockers:</p>
      </div>
{messages.map((msg, index) => (
  <div
    key={index}
    className={
      msg.user === selectedUser.name
        ? "message my-message"
        : "message other-message"
    }
  >
    <strong>{msg.user}</strong>

    <p style={{ whiteSpace: "pre-line" }}>
      {msg.text}
    </p>
  </div>
))}

    </div>
  );
}

export default StandupChat;