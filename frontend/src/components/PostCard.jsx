import { formatDate } from "../utils/formatDate";

function PostCard({ post }) {
  return (
    <article className="post-card">
      <div className="post-topline">
        <span className="post-badge">PUBLISHED</span>
        <time dateTime={post.createdAt}>{formatDate(post.createdAt)}</time>
      </div>

      <p className="post-text">{post.text}</p>

      <div className="rationale-box">
        <div className="section-label">WHY THIS WAS PUBLISHED</div>
        <p>{post.rationale}</p>
      </div>

      {post.sources?.length > 0 && (
        <div className="sources">
          <div className="section-label">LIVE SOURCES</div>
          {post.sources.map((source, index) => (
            <a
              key={`${source}-${index}`}
              href={source}
              target="_blank"
              rel="noreferrer"
            >
              <span>{new URL(source).hostname.replace("www.", "")}</span>
              <span aria-hidden="true">↗</span>
            </a>
          ))}
        </div>
      )}
    </article>
  );
}

export default PostCard;
