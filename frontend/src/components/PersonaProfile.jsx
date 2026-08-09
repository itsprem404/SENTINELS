function PersonaProfile({ profile }) {
  if (!profile) return null;

  const initial = profile.name
    ? profile.name.charAt(0).toUpperCase()
    : "A";

  return (
    <section className="persona-profile">

      {/* HEADER */}

      <div className="persona-header">

        <div className="persona-avatar">
          {initial}
        </div>

        <div className="persona-title">
          <span className="persona-label">
            ACTIVE PERSONA
          </span>

          <h2>
            {profile.name}
          </h2>

          <p>
            {profile.domain}
          </p>
        </div>

      </div>


      {/* DETAILS */}

      <div className="persona-details">

        <div className="persona-detail">
          <span>ROLE</span>
          <strong>
            {profile.role}
          </strong>
        </div>

        <div className="persona-detail">
          <span>DOMAIN</span>
          <strong>
            {profile.domain}
          </strong>
        </div>

        <div className="persona-detail persona-mission">
          <span>MISSION</span>
          <p>
            {profile.description}
          </p>
        </div>

      </div>

    </section>
  );
}

export default PersonaProfile;