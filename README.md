# AI-Powered Personalized Travel Itinerary Planner

**Plan Smarter. Travel Better.**

The AI-Powered Personalized Travel Itinerary Planner is a full-stack web application that builds a day-wise trip plan from your destination, number of days, budget, number of travelers, interests and travel style. Attractions across all Indian states and union territories are read from MongoDB, scored against your preferences, and arranged into realistic days with estimated entry costs and an interactive map.

> **Honesty note.** The attraction data is a **sample dataset** of 349 attractions in 82 destinations covering all 28 states and 8 union territories (a few major destinations per state, **not every location in India**). Entry costs and visit durations are rough estimates, coordinates are approximate (and missing for some places), ratings are intentionally `null`, and nothing is officially verified. The place ranking is **80% rule-based scoring plus a small machine-learning layer (20%)** that learns from the sample place text; the rules alone are not machine learning (see *Machine-learning layer*). The **AI features** (trip overview, day themes and tips, suggested visiting order, and a Q&A assistant) come from a real large language model (LLM) that you connect with your own API key; without a key they are switched off.

## Objectives
- Make trip planning faster, more personal and budget-friendly.
- Be transparent: estimates are labelled, missing data is shown as missing, never invented.
- Keep the code modular so a real ML/LLM recommender can be dropped in later.

## Features
- Destination search and state filter; planner dropdown grouped by state.
- Home page, trip planner form (with client + server validation), itinerary results with day-wise cards.
- **AI Travel Assistant (LLM):** personalised overview, day themes, tips and visiting order, plus "Ask the AI about this trip". Optional; needs `AI_API_KEY`.
- **Full trip cost estimate:** stay, food, local transport, your travel to the destination, entry fees and a 10% extras buffer, compared with your budget, plus the total under each travel style.
- Interactive Leaflet / OpenStreetMap map with popups for places that have stored coordinates.
- Sign up, log in, log out, profile; save, reopen and delete your own trips (JWT-protected).
- REST API with automatic docs at `/docs`.

## Technology stack
| Layer | Tools |
|---|---|
| Frontend | HTML5, CSS3, vanilla JavaScript, Leaflet.js, OpenStreetMap |
| Backend | Python, FastAPI, Pydantic |
| Database | MongoDB (Atlas), PyMongo, MongoDB Compass for browsing |
| Auth | JWT (PyJWT), bcrypt password hashing |
| Tests | Pytest, FastAPI TestClient |
| Deploy | GitHub, Render (or any Python host), MongoDB Atlas |

## System architecture
```
Browser (static/ SPA) --HTTP/JSON--> FastAPI routers  (app/routers)    request/response only
                                         |--> services   (app/services)   recommendation + itinerary logic (pure Python)
                                         |--> models     (app/models)     all MongoDB reads/writes (PyMongo)
                                         '--> schemas    (app/schemas)    Pydantic validation
                                                 |
                                          MongoDB Atlas: travel_planner_db
```
FastAPI serves both the API (`/api/...`) and the website (`/`), so one deployment is enough and no CORS setup is needed.

## Database structure (`travel_planner_db`)
| Collection | Fields | Indexes |
|---|---|---|
| `places` | name, city, state, categories, description, cost, hours, rating, latitude, longitude, source, verified (+ `cost_is_estimate`, `hours_is_estimate`, `coordinates_approximate`) | unique `(name, city)`, `city` |
| `users` | username, email, hashed_password, created_at | unique `email` |
| `trips` | user_id, destination, days, budget, travelers, interests, itinerary, estimated_total_cost, created_at | `(user_id, created_at)` |

Safety: only `travel_planner_db` is used. The code never drops databases or collections; seeding uses upserts keyed on `(name, city)`.

## Installation
Requires Python 3.10+.
```bash
cd travel_itinerary_planner
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## MongoDB Atlas setup
1. Create a free cluster at <https://www.mongodb.com/atlas>.
2. **Database Access** -> add a database user (username + password).
3. **Network Access** -> allow your IP for local work; for Render, add `0.0.0.0/0` (or Render's outbound IPs) and rely on a strong DB password.
4. **Connect -> Drivers** -> copy the connection string. You do not need to create the database or collections by hand; they are created on first write.
5. Optional: connect MongoDB Compass with the same string to browse `travel_planner_db`.

## Environment variables
```bash
cp .env.example .env     # then edit .env
```
| Variable | Meaning |
|---|---|
| `MONGODB_URI` | Atlas connection string (required) |
| `JWT_SECRET` | Random secret, 16+ chars (required). `python -c "import secrets; print(secrets.token_urlsafe(48))"` |
| `JWT_ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Login lifetime, default `30` |
| `CORS_ORIGINS` | Only if the frontend is on another domain |
| `SEED_ON_STARTUP` | `true` = run the safe upsert seed at startup |
| `AI_PROVIDER` | `anthropic` (Claude) or `gemini` (Google). Default `anthropic` |
| `AI_API_KEY` | Your LLM API key. Empty = AI features off |
| `AI_MODEL` | Optional model name; empty uses the provider default (`claude-haiku-5-5` / `gemini-2.0-flash`). For Gemini, if `AI_MODEL` is empty the app asks Google which models your key can use and picks the newest Flash model automatically. Run `python -m scripts.list_ai_models` to see them |
| `AI_RATE_LIMIT_PER_MINUTE` | Max AI calls per visitor per minute (default 10), to protect your bill |

## Seed the database
```bash
python -m scripts.seed_database --dry-run   # validate data/places.json only (no DB needed)
python -m scripts.seed_database             # upsert all 349 places into travel_planner_db.places
```
Safe to re-run: no duplicates, nothing deleted.

### Adding more places
Edit `scripts/dataset_source.py` (one line per attraction: name, categories, cost, hours, lat, lon, description; use `N` for unknown coordinates), then run `python -m scripts.build_dataset` to regenerate `data/places.json` and re-run the seed script. Only add coordinates, prices and ratings you can verify; leave them `N`/`None` otherwise. A test checks that `places.json` stays in sync with the source.

## Run the application
```bash
uvicorn app.main:app --reload
```
Open <http://127.0.0.1:8000> (website), <http://127.0.0.1:8000/docs> (API docs), <http://127.0.0.1:8000/api/health>.

## API documentation
| Method | Route | Auth | Purpose |
|---|---|---|---|
| POST | `/api/auth/register` | - | Create account, returns token |
| POST | `/api/auth/login` | - | Log in, returns token |
| GET | `/api/auth/me` | Bearer | Current user |
| GET | `/api/destinations` | - | Destinations with state and place counts |
| GET | `/api/destinations/{city}` | - | City details + its places |
| GET | `/api/places` | - | All places |
| GET | `/api/places/{city_or_place_id}` | - | Places in a city, **or** one place if the value is a 24-char id |
| POST | `/api/plan` | - | Generate an itinerary |
| GET | `/api/trips` | Bearer | Your saved trips (summaries) |
| POST | `/api/trips/save` | Bearer | Save an itinerary |
| GET | `/api/trips/{trip_id}` | Bearer | One of your trips (full itinerary) |
| DELETE | `/api/trips/{trip_id}` | Bearer | Delete one of your trips |
| GET | `/api/ai/status` | - | Whether AI is enabled, and which provider/model |
| POST | `/api/ai/insights` | - | AI overview, day themes, tips and order for an itinerary (rate-limited) |
| POST | `/api/ai/ask` | - | Ask the AI a question about an itinerary (rate-limited) |
| GET | `/api/health` | - | Health check (503 if MongoDB is unreachable) |

*Why one `/api/places/{...}` route:* `/places/{city}` and `/places/{place_id}` have identical shapes and would be duplicate routes, so a single route decides by the format of the value.

Example:
```bash
curl -X POST http://127.0.0.1:8000/api/plan -H "Content-Type: application/json" \
  -d '{"destination":"Jaipur","days":3,"budget":15000,"travelers":2,"interests":["history","culture"],"travel_style":"balanced"}'
```

## How the recommendation algorithm works
Every attraction in the chosen city gets a score from 0 to 1:

**Interests depend on the destination.** `GET /api/destinations` returns, for each city, how many attractions match each interest (`interest_counts`). The planner form only offers interests that exist at the chosen destination (for example Ujjain shows Culture and Religious places), with a count badge on each chip.

| Part | Weight | Idea |
|---|---|---|
| Interest match | 50% | How well the place's categories match what you picked (matching two interests counts as a full match) |
| Budget fit | 20% | Free/cheap entry scores high; cost is compared with a share (30%) of your budget for attractions |
| Rating | 20% | Used **only if a place has a real rating**. Otherwise this weight is removed and the others are scaled up. No ratings are invented. |
| Travel style | 10% | Budget -> cheaper places, Luxury -> longer visits, Balanced -> neutral |

Then the itinerary builder fills each day with the best places not yet used (never repeating one), stopping at 3-4 places or about 7 hours per day, skipping anything that would break your total budget, and preferring places near the day's first stop when coordinates exist. Straight-line distance is used only for that grouping, never shown as a road distance. Entry fees are `cost x travelers`.

### Full trip cost (`app/services/budget.py`)
`total = (stay + food + local transport + entry fees + travel to destination) x 1.10`

| Part | How it is estimated |
|---|---|
| Stay | rooms (2 travelers per room) x nights (default days - 1) x room rate |
| Food | travelers x days x food rate per person |
| Local transport | vehicles (4 travelers per cab/auto) x days x daily rate |
| Entry fees | from the itinerary |
| Travel to destination | you pick the mode (flight, train, bus, own car) and **enter** the round-trip cost per person (optional; 0 if blank). The app has no starting city, so it does not guess ticket prices |
| Extras | 10% buffer |

Rates depend on travel style (Budget / Balanced / Luxury) and destination type (metro / tourist / standard). They are **rough planning figures, not live prices**: edit `RATES` in `app/services/budget.py` to match your own research. If the total is over your budget, the app says by how much and shows what each travel style would cost.

To plug in a real ML or LLM ranker later, replace `score_place` / `rank_places` in `app/services/recommendation.py`; nothing else needs to change.

## How the AI part works
1. The rule-based engine (above) picks and orders the attractions from MongoDB. This part is deterministic and explainable.
2. When a visitor clicks **Generate AI insights**, the server sends a *compact copy of that itinerary* to the LLM and asks for JSON: title, overview, per-day theme, up to 3 tips, and a suggested order.
3. The reply is **validated**: only days and place names that exist in the itinerary are kept, a suggested order must be exactly that day's places, and all text is length-limited. Anything else is dropped.
4. **Ask the AI** answers questions using only the itinerary data and says to verify anything it does not know (prices, timings, transport).
5. The API key stays on the server (`.env` or Render settings), calls are rate-limited, and the UI always warns that AI text can be wrong. If the AI is off or fails, the itinerary still works.

Costs: LLM providers may charge per request (some offer a free tier). Check your provider's pricing and keep the rate limit low.

## Testing
```bash
pytest -v
```
Tests use an in-memory fake database (`tests/conftest.py`), never a real one. They cover health, register/login/invalid login, destinations, places, itinerary generation, budget/day/input validation, saving/listing/deleting trips and cross-user access protection. API tests are skipped automatically if FastAPI/httpx/bcrypt/pymongo are not installed.

## Deployment (GitHub + Render + Atlas)
1. `git init && git add . && git commit -m "Initial commit"` (`.env` is git-ignored; confirm with `git status`). Push to a new GitHub repository.
2. On Render: **New -> Blueprint** (uses `render.yaml`) or **New -> Web Service** with build `pip install -r requirements.txt` and start `uvicorn app.main:app --host 0.0.0.0 --port $PORT`; health check path `/api/health`.
3. Set environment variables in the Render dashboard: `MONGODB_URI`, `JWT_SECRET` (generated by the blueprint), and keep `SEED_ON_STARTUP=true` for the first deploy so the places load.
4. In Atlas **Network Access**, allow Render to connect (see step 3 of Atlas setup).
5. Open your `https://<service>.onrender.com` URL. The free tier sleeps when idle, so the first request can take ~30-60 seconds.

Separate frontend hosting (optional): set `window.APP_API_BASE = "https://your-api"` before `app.js` loads and set `CORS_ORIGINS` on the backend to the frontend's origin.

## Future enhancements
- Verified data: official ticket prices, opening hours, ratings and exact coordinates.
- More destinations, hotels and local transport; verified data feeds; admin tools to manage places.
- Real routing (e.g., OpenRouteService) for travel times, with graceful fallback.
- Use the LLM or a trained model to *rank* places as well (today it explains and enriches the rule-based result); streaming answers; conversation memory; saving AI chats.
- Live hotel/food/transport prices and ticket search; refresh tokens; rate limiting; photo hosting for place images.

## Known limitations
- Sample data only (349 places, not every location in India); about a third of coordinates are missing (shown as search links, not map pins); costs are estimates; no real photos are bundled (cards use illustrated placeholders). Add your own images under `static/images/`.
- Login token is kept in browser `localStorage` for simplicity.
- Stay, food and local transport use rough per-style rates (not live prices); intercity travel is only included if you enter it.


## Machine-learning layer (`app/services/ml.py`)

* **Method:** TF-IDF vectors of each place's text (name, description, city, state; category tags are hidden) and a **learned profile per interest** (average vector of all places tagged with it, a nearest-centroid classifier). A place's ML affinity is the cosine similarity to the profiles of the interests the traveller picked.
* **Weight:** 20% of the final score; the rule-based score keeps 80%. If scikit-learn is missing, the app falls back to rules only and says so (`algorithm.is_machine_learning`).
* **Trained on:** only the 349 sample places. No user data and no external dataset are used.
* **Evaluation:** `python -m scripts.evaluate_ml` runs 5-fold cross-validation with tags hidden. Result on this dataset: **mean ROC-AUC 0.85** (0.50 = guessing). The tags were written for this dataset, so treat the number as indicative, not as proof of real-world accuracy.
* **Limits:** descriptions are short, so the effect on rankings is modest.
