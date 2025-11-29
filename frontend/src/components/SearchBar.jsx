import PropTypes from 'prop-types'
import './SearchBar.css'

function SearchBar({ query, onChange, onSubmit, loading }) {
  return (
    <form className="search-bar" onSubmit={onSubmit}>
      <input
        type="text"
        value={query}
        placeholder="e.g. long sleeve navy A-line dress"
        onChange={onChange}
      />
      <button type="submit" disabled={loading || !query.trim()}>
        {loading ? 'Searching…' : 'Search'}
      </button>
    </form>
  )
}

SearchBar.propTypes = {
  query: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
  loading: PropTypes.bool,
}

SearchBar.defaultProps = {
  loading: false,
}

export default SearchBar
