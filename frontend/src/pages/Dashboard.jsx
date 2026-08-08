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

      if (!agentId) {
        setPosts([]);
        return;
      }


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


  function handleSwitchAgent() {

    const confirmed = window.confirm(
      "Switch agent?\n\nYour current agent will remain saved, but you will return to the agent setup screen."
    );


    if (!confirmed) {
      return;
    }


    localStorage.removeItem("agentId");

    setAgentId(null);

    setPosts([]);

  }


  return (

    <div className="dashboard">

      {/* =========================
          HEADER
      ========================= */}

      <header className="hero">

        <h1>SENTINELS</h1>

        <p>
          Autonomous AI Persona Dashboard
        </p>

      </header>



      {/* =========================
          CREATE AGENT
      ========================= */}

      {!agentId && (

        <section className="setup-section">

          <AgentSetup
            onAgentCreated={(id) => {

              localStorage.setItem(
                "agentId",
                id
              );

              setAgentId(id);

            }}
          />

        </section>

      )}



      {/* =========================
          AGENT DASHBOARD
      ========================= */}

      {agentId && (

        <>

          {/* AGENT STATUS */}

          <section className="status-grid">


            <div className="status-card">

              <div className="indicator"></div>

              <div>

                <h3>
                  Agent Active
                </h3>

                <p>
                  Autonomous monitoring enabled
                </p>

              </div>

            </div>



            <div className="info-card">

              <h3>
                Agent ID
              </h3>

              <code>
                {agentId.slice(0, 8)}
                ...
                {agentId.slice(-6)}
              </code>

            </div>



            <div className="info-card">

              <h3>
                Intelligence Reports
              </h3>

              <strong>
                {posts.length}
              </strong>

            </div>

          </section>



          {/* =========================
              AGENT CONTROLS
          ========================= */}

          <section className="agent-controls">

            <div>

              <span className="control-label">
                CURRENT AGENT
              </span>

              <p>
                Your autonomous intelligence persona is active.
              </p>

            </div>


            <button
              className="switch-agent-btn"
              onClick={handleSwitchAgent}
            >
              ⇄ Switch / Create Agent
            </button>

          </section>



          {/* =========================
              FEED HEADER
          ========================= */}

          <div className="feed-header">

            <h2>
              Latest Intelligence Feed
            </h2>

            <p>
              AI generated threat analysis and insights
            </p>

          </div>



          {/* =========================
              LOADING
          ========================= */}

          {loading && (

            <div className="loading">

              Analyzing intelligence streams...

            </div>

          )}



          {/* =========================
              EMPTY
          ========================= */}

          {!loading &&
            posts.length === 0 && (

              <div className="loading">

                No intelligence reports available.

              </div>

            )}



          {/* =========================
              POSTS
          ========================= */}

          {!loading && posts.length > 0 && (

            <div className="feed">

              {posts.map((post) => (

                <PostCard
                  key={post.id}
                  post={post}
                />

              ))}

            </div>

          )}

        </>

      )}

    </div>

  );
}


export default Dashboard;