const TAXONOMY = {
  silhouette: ['A-line', 'mermaid', 'sheath', 'ball gown', 'fit-and-flare'],
  length: ['mini', 'midi', 'knee-length', 'floor-length'],
  sleeve_type: ['sleeveless', 'short sleeve', 'long sleeve', 'off-shoulder'],
  color: ['red', 'blue', 'green', 'navy', 'black', 'white', 'pink'],
}

export function extractFilters(query) {
  if (!query) return {}
  const lowered = query.toLowerCase()
  const filters = {}

  Object.entries(TAXONOMY).forEach(([key, labels]) => {
    labels.forEach((label) => {
      if (lowered.includes(label.toLowerCase())) {
        filters[key] = label
      }
    })
  })

  return filters
}

export function formatFilters(filters) {
  const labelMap = {
    silhouette: 'Silhouette',
    length: 'Length',
    sleeve_type: 'Sleeve',
    color: 'Color',
  }

  return Object.entries(filters).map(([key, value]) => ({
    key,
    label: labelMap[key] ?? key,
    value,
  }))
}
