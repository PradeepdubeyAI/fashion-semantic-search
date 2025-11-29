import PropTypes from 'prop-types'

function ResultCard({ item }) {
  const { metadata } = item
  const imageSource = metadata?.source_url ?? metadata?.local_path ?? ''

  return (
    <article className="result-card">
      {imageSource ? (
        <img src={imageSource} alt={item.filename} loading="lazy" />
      ) : (
        <div className="placeholder" aria-label="Image unavailable" />
      )}
      <div className="result-body">
        <h3>{item.filename}</h3>
        <dl>
          <div>
            <dt>Silhouette</dt>
            <dd>{item.silhouette || 'Unknown'}</dd>
          </div>
          <div>
            <dt>Length</dt>
            <dd>{item.length || 'Unknown'}</dd>
          </div>
          <div>
            <dt>Sleeve</dt>
            <dd>{item.sleeve_type || 'Unknown'}</dd>
          </div>
          <div>
            <dt>Color</dt>
            <dd>{item.color || 'Unknown'}</dd>
          </div>
        </dl>
        {typeof item.similarity === 'number' && (
          <p className="similarity-badge">Match {(item.similarity * 100).toFixed(1)}%</p>
        )}
      </div>
    </article>
  )
}

ResultCard.propTypes = {
  item: PropTypes.shape({
    filename: PropTypes.string.isRequired,
    silhouette: PropTypes.string,
    length: PropTypes.string,
    sleeve_type: PropTypes.string,
    color: PropTypes.string,
    similarity: PropTypes.number,
    metadata: PropTypes.object,
  }).isRequired,
}

export default ResultCard
