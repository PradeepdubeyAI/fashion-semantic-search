import { useEffect, useMemo, useState } from 'react'
import './app.css'
import SearchBar from './components/SearchBar'
import FilterChips from './components/FilterChips'
import ResultsGrid from './components/ResultsGrid'
import { fetchImages, searchImages } from './api/client'

function App() {
  const [query, setQuery] = useState('')
  const [filters, setFilters] = useState({})
  const [results, setResults] = useState([])
  const [allImages, setAllImages] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    let active = true

    async function loadInitialImages() {
      try {
        setLoading(true)
        const data = await fetchImages()
        if (active) {
          setAllImages(data)
          setError('')
        }
      } catch (err) {
        setError(err.message)
      } finally {
        if (active) setLoading(false)
      }
    }

    loadInitialImages()
    return () => {
      active = false
    }
  }, [])

  const displayedItems = useMemo(() => (results.length ? results : allImages), [results, allImages])

  async function handleSearch() {
    if (!query.trim()) {
      setResults([])
      setFilters({})
      return
    }

    try {
      setLoading(true)
      const data = await searchImages(query)
      setResults(data.results ?? [])
      setFilters(data.filters ?? {})
      setError('')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-shell">
      <header>
        <h1>Dress Image Search</h1>
        <p>Search with natural language to find dresses by silhouette, length, sleeves, and more.</p>
      </header>

      <SearchBar
        query={query}
        onChange={(event) => setQuery(event.target.value)}
        onSubmit={(event) => {
          event.preventDefault()
          handleSearch()
        }}
        loading={loading}
      />

      <FilterChips filters={filters} />

      {error && <p className="error-message">{error}</p>}

      <ResultsGrid
        items={displayedItems}
        emptyMessage={query ? 'No dresses matched that description.' : 'No images ingested yet.'}
      />
    </div>
  )
}

export default App
