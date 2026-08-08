import { useState } from "react";
import { initializeAgent } from "../api/agentApi";

function AgentSetup({ onAgentCreated }) {

    const [name, setName] = useState("");
    const [domain, setDomain] = useState("");
    const [loading, setLoading] = useState(false);


    async function handleSubmit(e) {
        e.preventDefault();

        try {
            setLoading(true);

            const response = await initializeAgent({
                name,
                domain
            });

            localStorage.setItem(
                "agentId",
                response.agentId
            );

            onAgentCreated(response.agentId);

        } catch (error) {
            console.error(error);
            alert("Agent initialization failed");
        }
        finally {
            setLoading(false);
        }
    }


    return (
        <div>
            <h2>Create AI Persona</h2>

            <form onSubmit={handleSubmit}>

                <input
                    type="text"
                    placeholder="Persona Name"
                    value={name}
                    onChange={(e)=>setName(e.target.value)}
                    required
                />

                <input
                    type="text"
                    placeholder="Domain (AI Security etc.)"
                    value={domain}
                    onChange={(e)=>setDomain(e.target.value)}
                    required
                />

                <button type="submit" disabled={loading}>
                    {loading ? "Creating..." : "Create Agent"}
                </button>

            </form>

        </div>
    );
}

export default AgentSetup;