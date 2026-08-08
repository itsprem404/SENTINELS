import { useState } from "react";
import { initializeAgent } from "../api/agentApi";

function AgentSetup({ onAgentCreated }) {
  const [form, setForm] = useState({
    name: "",
    domain: "",
    role: "",
    description: "",
  });

  const [loading, setLoading] = useState(false);

  function handleChange(e) {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  }

  async function handleSubmit(e) {
    e.preventDefault();

    try {
      setLoading(true);

      const response = await initializeAgent({
        name: form.name,
        domain: form.domain,
        role: form.role,
        description: form.description,
      });

      localStorage.setItem("agentId", response.agentId);

      onAgentCreated(response.agentId);
    } catch (error) {
      console.error("Agent initialization failed:", error);

      alert("Agent initialization failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="setup-container">
      <div className="setup-card">
        <div className="setup-header">
          <div className="agent-icon">🛰️</div>

          <h2>Create Intelligence Agent</h2>

          <p>Configure your autonomous AI persona</p>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label>Agent Name</label>

            <input
              name="name"
              type="text"
              placeholder="Cyber Sentinel"
              value={form.name}
              onChange={handleChange}
              required
            />
          </div>

          <div className="input-group">
            <label>Intelligence Domain</label>

            <input
              name="domain"
              type="text"
              placeholder="Cybersecurity"
              value={form.domain}
              onChange={handleChange}
              required
            />
          </div>

          <div className="input-group">
            <label>Agent Role</label>

            <input
              name="role"
              type="text"
              placeholder="Threat Intelligence Analyst"
              value={form.role}
              onChange={handleChange}
              required
            />
          </div>

          <div className="input-group">
            <label>Mission Description</label>

            <textarea
              name="description"
              placeholder="Monitor cybersecurity threats and generate intelligence reports"
              value={form.description}
              onChange={handleChange}
              rows="4"
              required
            />
          </div>

          <button type="submit" disabled={loading}>
            {loading ? "Initializing Agent..." : "🚀 Launch AI Agent"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default AgentSetup;
