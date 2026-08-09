const API_BASE_URL = "http://127.0.0.1:8000/api/agent";

export async function initializeAgent(persona) {
  const response = await fetch(`${API_BASE_URL}/init`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      persona,
    }),
  });

  if (!response.ok) {
    throw new Error("Agent initialization failed");
  }

  return await response.json();
}

export async function getFeed(agentId) {
  const response = await fetch(`${API_BASE_URL}/feed?agentId=${agentId}`);

  if (!response.ok) {
    throw new Error("Failed to fetch feed");
  }

  return await response.json();
}

export async function getProfile(agentId) {
  const response = await fetch(
    `${API_BASE_URL}/profile?agentId=${agentId}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch agent profile");
  }

  return await response.json();
}