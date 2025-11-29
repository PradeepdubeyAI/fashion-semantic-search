import PropTypes from 'prop-types'

function FilterChips({ filters }) {
  const entries = Object.entries(filters).filter(([, value]) => Boolean(value))

  if (!entries.length) {
    return null
  }

  return (
    <div className="filter-chips">
      {entries.map(([key, value]) => (
        <span key={key} className="filter-chip">
          <span className="filter-label">{key.replace('_', ' ')}</span>
          <span className="filter-value">{value}</span>
        </span>
      ))}
    </div>
  )
}

FilterChips.propTypes = {
  filters: PropTypes.object,
}

FilterChips.defaultProps = {
  filters: {},
}

export default FilterChips
