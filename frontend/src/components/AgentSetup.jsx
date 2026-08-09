import { useState } from "react";
import { initializeAgent } from "../api/agentApi";

const initialForm = {
  name: "",
  domain: "",
  role: "",
  description: "",
};

function AgentSetup({ onAgentCreated }) {
  const [form, setForm] = useState(initialForm);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function handleChange(event) {
    setForm((current) => ({ ...current, [event.target.name]: event.target.value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");

    try {
      setLoading(true);
      const response = await initializeAgent({
        name: form.name.trim(),
        domain: form.domain.trim(),
        role: form.role.trim() || undefined,
        description: form.description.trim() || undefined,
      });
      localStorage.setItem("agentId", response.agentId);
      onAgentCreated(response.agentId);
    } catch (err) {
      setError(err.message || "Agent initialization failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="setup-container">
      <div className="setup-card">
        <div className="setup-header">
          <div className="agent-icon">◈</div>
          <div className="eyebrow">AUTONOMOUS CREATOR</div>
          <h2>Initialize your Sentinel</h2>
          <p>
            Give it an identity once. It will research, judge, remember and
            publish without another prompt.
          </p>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="name">Persona name</label>
            <input
              id="name"
              name="name"
              type="text"
              placeholder="Persona Name"
              value={form.name}
              onChange={handleChange}
              maxLength={80}
              required
            />
          </div>

          <div className="input-group">
            <label htmlFor="domain">Technology domain</label>
            <input
              id="domain"
              name="domain"
              type="text"
              placeholder="Domain Name (Ex: AI Security)"
              value={form.domain}
              onChange={handleChange}
              maxLength={120}
              required
            />
          </div>

          <details className="advanced-fields">
            <summary>Optional persona details</summary>

            <div className="input-group">
              <label htmlFor="role">Role</label>
              <input
                id="role"
                name="role"
                type="text"
                placeholder="Ex: AI Security Researcher"
                value={form.role}
                onChange={handleChange}
              />
            </div>

            <div className="input-group">
              <label htmlFor="description">Mission</label>
              <textarea
                id="description"
                name="description"
                placeholder="Ex: Track meaningful security changes in AI systems and developer infrastructure."
                value={form.description}
                onChange={handleChange}
                rows="3"
              />
            </div>
          </details>

          {error && <div className="form-error">{error}</div>}

          <button type="submit" disabled={loading}>
            {loading ? "Initializing..." : "Launch autonomous agent"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default AgentSetup;
