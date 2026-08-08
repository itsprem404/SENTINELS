function PostCard({ post }) {
  return (
    <div className="post-card">
      <h2>{post.text}</h2>

      <p className="rationale">{post.rationale}</p>

      <div className="meta">
        <span>🕒 {new Date(post.createdAt).toLocaleString()}</span>
      </div>

      {post.sources?.length > 0 && (
        <div className="sources">
          <strong>Sources:</strong>

          {post.sources.map((source, index) => (
            <a key={index} href={source} target="_blank">
              {source}
            </a>
          ))}
        </div>
      )}
    </div>
  );
}

export default PostCard;
