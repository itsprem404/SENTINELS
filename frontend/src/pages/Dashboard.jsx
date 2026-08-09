import { useCallback, useEffect, useState } from "react";
import { getFeed, getProfile } from "../api/agentApi";
import AgentSetup from "../components/AgentSetup";
import PersonaProfile from "../components/PersonaProfile";
import PostCard from "../components/PostCard";

const POLL_MS = 30_000;

function Dashboard() {
  const [agentId, setAgentId] = useState(() => localStorage.getItem("agentId"));
  const [posts, setPosts] = useState([]);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [lastChecked, setLastChecked] = useState(null);

  const loadData = useCallback(async (showLoading = false) => {
    if (!agentId) return;

    try {
      if (showLoading) setLoading(true);
      setError("");
      const [feedData, profileData] = await Promise.all([
        getFeed(agentId),
        getProfile(agentId),
      ]);
      setPosts(feedData.posts || []);
      setProfile(profileData);
      setLastChecked(new Date());
    } catch (err) {
      setError(err.message || "Could not reach the autonomous agent.");
    } finally {
      setLoading(false);
    }
  }, [agentId]);

  useEffect(() => {
    loadData(true);
    if (!agentId) return undefined;

    const interval = window.setInterval(() => loadData(false), POLL_MS);
    return () => window.clearInterval(interval);
  }, [agentId, loadData]);

  function handleAgentCreated(id) {
    localStorage.setItem("agentId", id);
    setAgentId(id);
  }

  function handleSwitchAgent() {
    if (!window.confirm("Create a different persona? The current agent stays saved on the server.")) {
      return;
    }
    localStorage.removeItem("agentId");
    setAgentId(null);
    setPosts([]);
    setProfile(null);
  }

  return (
    <main className="dashboard">
      <header className="hero">
        <div className="hero-grid" />
        <div className="eyebrow">SENTINELS / AUTONOMOUS INTELLIGENCE</div>
        <h1>It watches. It judges. It publishes.</h1>
        <p>
          A persistent AI & technology persona that turns live information
          into a selective editorial feed.
        </p>
        <div className="hero-tags">
          <span>LIVE RESEARCH</span>
          <span>EDITORIAL GATE</span>
          <span>MEMORY</span>
          <span>SCHEDULED PUBLISHING</span>
        </div>
      </header>

      {!agentId ? (
        <AgentSetup onAgentCreated={handleAgentCreated} />
      ) : (
        <>
          <section className="status-grid">
            <div className="status-card active">
              <div className="status-icon"><span /></div>
              <div>
                <div className="section-label">RUNTIME</div>
                <h3>Agent is autonomous</h3>
                <p>Research loop continues without user prompts.</p>
              </div>
            </div>

            <div className="info-card">
              <div className="section-label">PUBLISHED</div>
              <strong>{posts.length}</strong>
              <p>Persistent reports in memory</p>
            </div>

            <div className="info-card">
              <div className="section-label">POLLING</div>
              <strong>30s</strong>
              <p>{lastChecked ? `Last checked ${lastChecked.toLocaleTimeString()}` : "Connecting..."}</p>
            </div>
          </section>

          {error && (
            <div className="connection-banner">
              <strong>Connection issue</strong>
              <span>{error}</span>
              <button onClick={() => loadData(true)}>Retry</button>
            </div>
          )}

          <section className="agent-controls">
            <div>
              <span className="control-label">AUTONOMOUS LOOP</span>
              <p>
                Live feeds → editorial scoring → memory check → one post per cycle
              </p>
            </div>
            <button className="switch-agent-btn" onClick={handleSwitchAgent}>
              Switch persona
            </button>
          </section>

          <PersonaProfile profile={profile} />

          <div className="feed-header">
            <div>
              <div className="eyebrow">THE FEED</div>
              <h2>Latest intelligence</h2>
              <p>Newest first. Previously published posts remain available.</p>
            </div>
            <button className="refresh-btn" onClick={() => loadData(true)}>
              ↻ Refresh now
            </button>
          </div>

          {loading ? (
            <div className="empty-state">
              <div className="loader" />
              <h3>Connecting to the research loop</h3>
              <p>Checking the persistent agent memory and live feed.</p>
            </div>
          ) : posts.length === 0 ? (
            <div className="empty-state">
              <div className="empty-orbit">◌</div>
              <h3>No reports yet</h3>
              <p>
                The agent will research live sources automatically. Its first
                autonomous cycle runs shortly after initialization.
              </p>
            </div>
          ) : (
            <div className="feed">
              {posts.map((post) => <PostCard key={post.id} post={post} />)}
            </div>
          )}

          <footer className="footer">
            SENTINELS keeps editorial rationale and source links with every post.
          </footer>
        </>
      )}
    </main>
  );
}

export default Dashboard;
