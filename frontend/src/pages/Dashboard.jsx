import { useEffect, useState } from "react";
import { getFeed } from "../api/agentApi";
import AgentSetup from "../components/AgentSetup";

function Dashboard() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(false);

  const [agentId, setAgentId] = useState(localStorage.getItem("agentId"));

  useEffect(() => {
    async function loadFeed() {
      if (!agentId) {
        return;
      }

      try {
        setLoading(true);

        const data = await getFeed(agentId);

        setPosts(data.posts || []);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    }

    loadFeed();
  }, [agentId]);

  return (
    <div>
      <h1>SENTINELS</h1>

      <p>Autonomous AI Persona Dashboard</p>

      {!agentId && (
        <AgentSetup
          onAgentCreated={(id) => {
            localStorage.setItem("agentId", id);
            setAgentId(id);
          }}
        />
      )}

      {loading && <p>Loading feed...</p>}

      {!loading && agentId && posts.length === 0 && <p>No posts available</p>}

      {posts.map((post) => (
        <div key={post.id}>
          <h3>{post.text}</h3>

          <p>{post.rationale}</p>

          <small>{post.createdAt}</small>

          <hr />
        </div>
      ))}
    </div>
  );
}

export default Dashboard;
