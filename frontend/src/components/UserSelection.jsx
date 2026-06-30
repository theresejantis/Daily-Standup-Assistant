function UserSelection({ onSelectUser }) {
  const users = [
    { id: 1, name: "Therese", role: "Employee" },
    { id: 2, name: "John", role: "Employee" },
    { id: 3, name: "Alex", role: "Employee" },
    { id: 4, name: "Manager", role: "Manager" },
  ];

  return (
    <div className="selection-page">
      <div className="selection-card">

        <h1>Daily Standup Assistant</h1>

        <p className="subtitle">
          AI Powered Daily Standup & Progress Tracking
        </p>

        <h2>Select User</h2>

        <div className="user-grid">
          {users.map((user) => (
            <button
              key={user.id}
              className="user-card"
              onClick={() => onSelectUser(user)}
            >
              <div className="user-avatar">
                {user.role === "Manager" ? "👔" : "👤"}
              </div>

              <h3>{user.name}</h3>

              <span>{user.role}</span>
            </button>
          ))}
        </div>

      </div>
    </div>
  );
}

export default UserSelection;