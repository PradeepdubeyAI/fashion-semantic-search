import PropTypes from 'prop-types'
import ResultCard from './ResultCard'

function ResultsGrid({ items, emptyMessage }) {
  if (!items.length) {
    return <p className="empty-state">{emptyMessage}</p>
  }

  return (
    <section className="results-grid">
      {items.map((item) => (
        <ResultCard key={item.id} item={item} />
      ))}
    </section>
  )
}

ResultsGrid.propTypes = {
  items: PropTypes.arrayOf(PropTypes.object),
  emptyMessage: PropTypes.string,
}

ResultsGrid.defaultProps = {
  items: [],
  emptyMessage: 'No dresses found for that query.',
}

export default ResultsGrid
