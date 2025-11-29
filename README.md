# Dress Image Search System

End-to-end image search demo that indexes dress photos, extracts fashion attributes with local models, and exposes both attribute- and embedding-based search through a FastAPI backend and React frontend.

## Project Structure

```
backend/
  app/
    config.py            # FastAPI configuration with CORS (localhost:5173, 5174)
    db.py                # SQLite helpers and schema (images + embeddings tables)
    main.py              # API endpoints: /health, /images, /search, /upload-images
    services/
      model_loader.py    # Singleton for CLIP (sentence-transformers) + spaCy models
      processor.py       # Zero-shot attribute extraction + spaCy query parsing
      ingestion.py       # Shared URL download + CLIP embedding + DB persist
  images/                # Downloaded dress images (created at runtime)
  ingest.py              # CLI script: bulk ingest CSV URLs → extract attributes → index
  taxonomy.json          # Fashion attribute taxonomy (silhouette, length, sleeve, color)
  dress_search.db        # SQLite database with 10+ indexed dresses
  requirements.txt       # Python dependencies
frontend/
  src/
    api/client.js        # HTTP client for /images and /search endpoints
    components/
      SearchBar.jsx      # Natural language query input
      FilterChips.jsx    # Visual display of extracted filters
      ResultCard.jsx     # Individual dress card with metadata
      ResultsGrid.jsx    # Responsive grid layout
    app.jsx              # Main App component with state + search logic
    index.css            # Global styles
    app.css              # Component styles (grid, cards, responsive design)
  vite.config.js         # Vite build configuration
  package.json           # Node.js dependencies
taxonomy.json            # (symlink or copy from backend/)
README.md                # (this file)
```

## Prerequisites

- **Python 3.11+** (for backend)
- **Node.js 20+** (for frontend)
- **Modern browser** (Chrome, Firefox, Safari, Edge)
- **CSV file** with image URLs (e.g., `test2.csv` with one URL per line)

> **Local-only AI**: All AI runs locally. No cloud APIs.
> - **CLIP** (sentence-transformers ViT-B-32): ~605 MB, downloaded on first run
> - **spaCy** (en_core_web_sm): ~50 MB, downloaded on first setup
> - **Taxonomy**: Externalized from `taxonomy.json` 

## Backend Setup

1. **Create and activate virtual environment**
   ```powershell
   cd backend
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

2. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3. **Ingest dataset from CSV**
   ```powershell
   python ingest.py "path/to/test2.csv"
   ```
   - **What it does:**
     - Downloads each image URL to `backend/images/`
     - Runs CLIP zero-shot classification to extract: silhouette, length, sleeve_type, color
     - Generates CLIP embeddings (512-dim vectors) for semantic search
     - Stores metadata + embeddings in `backend/dress_search.db` (SQLite)
   - **Expected output:** 10 images indexed (2 may fail due to network/SSL)

4. **Start the API server**
   ```powershell
   # Make sure you are in the backend directory!
   cd backend
   
   # Then run uvicorn
   uvicorn app.main:app --host localhost --port 8000
   ```
   or use `--reload` for development:
   ```powershell
   cd backend
   uvicorn app.main:app --reload --host localhost --port 8000
   ```
   > ⚠️ **Important:** Always run `cd backend` first before running uvicorn. The `app` module is inside the `backend/app/` directory.
   
   - API ready at `http://localhost:8000`

### API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/health` | Health check → `{"status": "ok"}` |
| `GET` | `/images` | List all 10 indexed dresses (no embeddings) |
| `POST` | `/search` | Search with natural language query |
| `POST` | `/upload-images` | Add new image URLs on-the-fly |

**Search Example:**
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "navy A-line long sleeve floor-length dress"}'
```

**Response:**
```json
{
  "filters": {
    "color": "navy",
    "silhouette": "A-line",
    "sleeve_type": "long sleeve",
    "length": "floor-length"
  },
  "results": [
    {
      "id": 1,
      "filename": "...",
      "color": "navy",
      "silhouette": "ball gown",
      "similarity": 0.4521
    },
    ...
  ]
}
```

### Environment Variables (Optional)

Create `.env` in `backend/` directory:
```env
DRESS_SEARCH_FRONTEND_ORIGIN=http://localhost:5173
DRESS_SEARCH_APP_NAME=Dress Search API
```

Or set via command line (Windows PowerShell):
```powershell
$env:DRESS_SEARCH_FRONTEND_ORIGIN="http://localhost:5173"
```

## Frontend Setup

The frontend connects to the backend at `http://localhost:8000`.

```powershell
cd frontend
npm install
npm run dev
```

- Opens on `http://localhost:5173` (or 5174 if 5173 is busy)
- Search bar accepts natural language queries
- Filter chips show extracted attributes
- Results grid displays all matching dresses with similarity scores

### Production Build

```powershell
npm run build
npm run preview
```

### Override Backend URL

Create `frontend/.env`:
```
VITE_API_BASE_URL=http://your-backend-host:8000
```

Or use environment variable before running:
```powershell
$env:VITE_API_BASE_URL="http://your-backend:8000"; npm run dev
```



### How It Works

1. **Query Parsing (spaCy)**
   - Tokenize and lemmatize user input
   - Match keywords against `taxonomy.json`
   - Extract structured filters (e.g., "navy long sleeve" → `{color: navy, sleeve_type: long sleeve}`)

2. **SQL Pre-filtering**
   - Query images matching extracted filters
   - Fallback to all images if no exact matches found (enables fuzzy search)

3. **CLIP Embedding & Ranking**
   - Encode query text using CLIP: `query → 512-dim vector`
   - Compute cosine similarity between query and each dress embedding
   - Sort by similarity (highest first)

4. **Response Format**
   ```json
   {
     "filters": {"color": "navy", "sleeve_type": "long sleeve"},
     "results": [
       {
         "id": 1,
         "filename": "...",
         "color": "navy",
         "silhouette": "ball gown",
         "length": "floor-length",
         "sleeve_type": "off-shoulder",
         "similarity": 0.4521
       }
     ]
   }
   ```

## Testing & Validation

### Quick Test (API Only)

```powershell
cd backend
python test_search.py
```

Expected output:
```
✅ Health: 200
✅ Search: 200
   Filters: {'sleeve_type': 'long sleeve', 'color': 'navy'}
   Results: 10 matches
   Top result: navy ball gown (similarity: 0.169)
```

### Manual Browser Test

1. **Start backend:**
   ```powershell
   cd backend
   uvicorn app.main:app --host localhost --port 8000
   ```

2. **Start frontend (new terminal):**
   ```powershell
   cd frontend
   npm run dev
   ```

3. **Open browser:**
   - Navigate to `http://localhost:5173`

### Test Examples

Try these search queries on the UI. Each will extract filters and return ranked results:

| Query | Expected Filters | What to Verify |
|-------|-----------------|-----------------|
| **"navy long sleeve"** | `color: navy, sleeve_type: long sleeve` | Returns 10 images, top match navy ball gown |
| **"red ball gown"** | `color: red, silhouette: ball gown` | Returns red dresses sorted by similarity |
| **"A-line dress"** | `silhouette: A-line` | Returns A-line silhouettes |
| **"sleeveless mermaid"** | `sleeve_type: sleeveless, silhouette: mermaid` | Returns sleeveless mermaid dresses |
| **"floor-length"** | `length: floor-length` | Returns full-length dresses |
| **"short sleeve blue"** | `sleeve_type: short sleeve, color: blue` | Returns blue dresses with short sleeves |
| **"white fit and flare"** | `color: white, silhouette: fit-and-flare` | Returns white fit-and-flare dresses |
| **"pink dress"** | `color: pink` | Returns all pink dresses |

**What you should see:**
- ✅ Search bar accepts natural language
- ✅ Filter chips appear showing extracted attributes
- ✅ Dress images load in a grid
- ✅ Each card shows: image, filename, color, silhouette, sleeve type, length
- ✅ Results ranked by similarity score (0-1)

### Troubleshooting

| Issue | Solution |
|-------|----------|
| **`ModuleNotFoundError: No module named 'app'`** | Make sure you're in the `backend/` directory. Run `cd backend` first, then `uvicorn app.main:app --host localhost --port 8000` |
| **Backend won't start** | Check port 8000 is free: `netstat -ano \| findstr :8000` |
| **CLIP download slow** | First run downloads ~605MB model. This is normal (3-5 min) |
| **spaCy download fails** | Run manually: `python -m spacy download en_core_web_sm` |
| **Frontend shows "Failed to fetch"** | Ensure backend is running on 8000; check CORS in `app/config.py` |
| **Images not loading** | Check `backend/images/` directory exists; re-run `ingest.py` |
| **SQLite locked** | Stop backend server before re-running `ingest.py` |
| **Port 5173 in use** | Frontend will try 5174, 5175, etc. automatically |

## Architecture & Design Decisions

### Why Hybrid Search?

**Problem:** Pure semantic search (CLIP alone) can miss exact matches. Pure SQL filtering is rigid.

**Solution:** Combine both:
- SQL for **exact attribute matching** (fast, deterministic)
- CLIP for **semantic relevance** (captures intent, synonyms, context)
- Fallback to all images if SQL returns 0 (enables fuzzy discovery)

### Why Taxonomy as JSON?

- **Externalized:** Easy to update without code changes
- **Maintainable:** Add/remove fashion categories dynamically
- **Portable:** Can be loaded from database later if needed

### Why spaCy + CLIP?

- **spaCy** for linguistic structure (lemmatization, token dependency)
- **CLIP** for zero-shot vision-language alignment (no labeled training data needed)
- **Lightweight:** Both run on CPU; no GPU required

### Scalability Notes

- **Current:** 10 images, SQLite, single process
- **Next step:** Vector DB (Qdrant, Pinecone) for 1M+ images
- **Deployment:** Docker + FastAPI + React frontend

## File Descriptions

### Backend Core

- **`app/main.py`** – FastAPI app, endpoints, CORS, startup hooks
- **`app/db.py`** – SQLite schema (images + embeddings), insert/fetch queries
- **`app/config.py`** – Pydantic settings, environment variable overrides
- **`app/services/model_loader.py`** – Singleton CLIP + spaCy loader (LRU cache)
- **`app/services/processor.py`** – Zero-shot classification, query parsing, embedding generation
- **`app/services/ingestion.py`** – URL download, attribute extraction, DB persist

### Frontend Components

- **`src/app.jsx`** – Main App (state, effects, event handlers)
- **`src/components/SearchBar.jsx`** – Input + submit button
- **`src/components/FilterChips.jsx`** – Visual filter display
- **`src/components/ResultCard.jsx`** – Individual dress card
- **`src/components/ResultsGrid.jsx`** – Responsive grid layout
- **`src/api/client.js`** – HTTP wrapper for `/images` and `/search`
- **`src/app.css`** – Component styles (grid, cards, responsive)
- **`src/index.css`** – Global styles (fonts, colors, theme)
