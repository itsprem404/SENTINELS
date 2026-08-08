import { useState } from "react";
import AgentSetup from "../components/AgentSetup";

function Dashboard() {
  const [agentId, setAgentId] = useState(localStorage.getItem("agentId"));

  function handleAgentCreated(id) {
    setAgentId(id);
  }

  return (
    <div>
      <h1>SENTINELS</h1>
      <p>Autonomous AI Persona Dashboard</p>

      {agentId ? (
        <div>
          <h3>Agent Initialized</h3>

          <p>Agent ID: {agentId}</p>
        </div>
      ) : (
        <AgentSetup onAgentCreated={handleAgentCreated} />
      )}
    </div>
  );
}

export default Dashboard;
