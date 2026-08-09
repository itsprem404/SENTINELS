const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "/api/agent";

async function request(url, options) {
  const response = await fetch(url, options);

  if (!response.ok) {
    let message = `Request failed (${response.status})`;

    try {
      const data = await response.json();
      message = data.detail || message;
    } catch {}

    const error = new Error(message);
    error.status = response.status;

    throw error;
  }

  return response.json();
}

export function initializeAgent(persona) {
  return request(`${API_BASE_URL}/init`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ persona }),
  });
}

export function getFeed(agentId) {
  return request(
    `${API_BASE_URL}/feed?agentId=${encodeURIComponent(agentId)}`
  );
}

export function getProfile(agentId) {
  return request(
    `${API_BASE_URL}/profile?agentId=${encodeURIComponent(agentId)}`
  );
}