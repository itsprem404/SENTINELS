import { useEffect, useState } from "react";
import { getFeed } from "../api/agentApi";

import AgentSetup from "../components/AgentSetup";
import PostCard from "../components/PostCard";

function Dashboard() {
  const [posts, setPosts] = useState([]);

  const [loading, setLoading] = useState(false);

  const [agentId, setAgentId] = useState(() => {
  return localStorage.getItem("agentId");
  });

  useEffect(() => {
    async function loadFeed() {
      if (!agentId) return;

      try {
        setLoading(true);

        const data = await getFeed(agentId);

        setPosts(data.posts || []);
      } catch (error) {
        console.error("Feed error:", error);
      } finally {
        setLoading(false);
      }
    }

    loadFeed();
  }, [agentId]);

  return (
    <div className="dashboard">
      {/* HEADER */}

      <header className="hero">
        <h1>SENTINELS</h1>

        <p>Autonomous AI Persona Dashboard</p>
      </header>

      {/* CREATE AGENT */}

      {!agentId && (
        <section className="setup-section">
          <h2>Create Intelligence Agent</h2>

          <AgentSetup
            onAgentCreated={(id) => {
              localStorage.setItem("agentId", id);

              setAgentId(id);
            }}
          />
        </section>
      )}

      {/* AGENT STATUS */}

      {agentId && (
        <section className="status-grid">
          <div className="status-card">
            <div className="indicator"></div>

            <div>
              <h3>Agent Active</h3>

              <p>Autonomous monitoring enabled</p>
            </div>
          </div>

          <div className="info-card">
            <h3>Agent ID</h3>

            <code>
              {agentId.slice(0, 8)}...{agentId.slice(-6)}
            </code>
          </div>

          <div className="info-card">
            <h3>Intelligence Reports</h3>

            <strong>{posts.length}</strong>
          </div>
        </section>
      )}

      {/* FEED HEADER */}

      {agentId && (
        <div className="feed-header">
          <h2>Latest Intelligence Feed</h2>

          <p>AI generated threat analysis and insights</p>
        </div>
      )}

      {/* LOADING */}

      {loading && (
        <div className="loading">Analyzing intelligence streams...</div>
      )}

      {/* EMPTY */}

      {!loading && agentId && posts.length === 0 && (
        <p>No intelligence reports available.</p>
      )}

      {/* POSTS */}

      <div className="feed">
        {posts.map((post) => (
          <PostCard key={post.id} post={post} />
        ))}
      </div>
    </div>
  );
}

export default Dashboard;
