const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

async function handleResponse(response) {
  if (!response.ok) {
    const body = await response.text()
    throw new Error(body || 'Request failed')
  }
  return response.json()
}

export async function fetchImages() {
  const response = await fetch(`${API_BASE_URL}/images`)
  return handleResponse(response)
}

export async function searchImages(query) {
  const response = await fetch(`${API_BASE_URL}/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }),
  })
  return handleResponse(response)
}

export async function uploadImages(urls) {
  const response = await fetch(`${API_BASE_URL}/upload-images`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ urls }),
  })
  return handleResponse(response)
}
