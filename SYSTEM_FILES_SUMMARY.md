# System Files Summary

## Backend

### Core API
- `backend/app/main.py` – FastAPI application with 4 endpoints (/health, /images, /search, /upload-images)
- `backend/app/config.py` – Pydantic settings with CORS configuration
- `backend/app/db.py` – SQLite helper functions and schema (images + embeddings tables)

### Services
- `backend/app/services/model_loader.py` – Singleton CLIP + spaCy model loader with LRU cache
- `backend/app/services/processor.py` – Zero-shot attribute extraction, query parsing, text/image embeddings
- `backend/app/services/ingestion.py` – Shared URL download, attribute extraction, database persistence

### Configuration & Dependencies
- `backend/taxonomy.json` – Externalized fashion attribute taxonomy (NOT hardcoded)
- `backend/requirements.txt` – Python dependencies with detailed comments
- `backend/ingest.py` – CLI script for bulk ingestion from CSV files

### Runtime Data
- `backend/dress_search.db` – SQLite database (auto-created, contains 10+ indexed dresses)
- `backend/images/` – Directory for downloaded dress images (auto-created)

## Frontend

### Components
- `frontend/src/app.jsx` – Main React App component with state management
- `frontend/src/components/SearchBar.jsx` – Query input + submit button
- `frontend/src/components/FilterChips.jsx` – Filter visualization
- `frontend/src/components/ResultCard.jsx` – Individual dress display
- `frontend/src/components/ResultsGrid.jsx` – Responsive grid layout

### API Integration
- `frontend/src/api/client.js` – HTTP wrapper for backend endpoints

### Styling
- `frontend/src/app.css` – Component-specific styles
- `frontend/src/index.css` – Global styles and theme

### Build Configuration
- `frontend/vite.config.js` – Vite bundler configuration
- `frontend/package.json` – Node.js dependencies

## Documentation
- `README.md` – Comprehensive setup, usage, and architecture guide
- `SYSTEM_FILES_SUMMARY.md` – This file

## Testing Scripts (Optional)
- `backend/test_api.py` – Full API verification suite
- `backend/test_search.py` – Search endpoint test with sample queries
- `backend/test_search_logic.py` – Isolated search logic testing
- `backend/debug_db.py` – Database inspection and debugging
- `backend/verify_taxonomy.py` – Taxonomy loading verification
- `backend/test_searches.py` – Multiple search query testing
- `final_verification.py` – Comprehensive end-to-end system test

## Key Features

✅ **Local AI Only** – CLIP + spaCy (no external APIs)
✅ **Hybrid Search** – SQL pre-filtering + CLIP semantic ranking
✅ **Externalized Config** – taxonomy.json (not hardcoded)
✅ **REST API** – FastAPI with 4 endpoints
✅ **React Frontend** – Responsive UI with filter chips + results grid
✅ **Database** – SQLite with image metadata + embeddings
✅ **Production Ready** – CORS handling, error management, environment config

## Quick Start

```bash
# Backend
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python ingest.py "path/to/test2.csv"
uvicorn app.main:app --host localhost --port 8000

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

Then open `http://localhost:5173` and search for dresses!
