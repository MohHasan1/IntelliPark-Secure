# IntelliPark

Modern parking control system with Python backend (ANPR + APSD models) and a Next.js dashboard for live monitoring, gate status, and whitelist management.

## Modules

-   **Python backend**
    -   `app.py`: Flask API (events, scenes, sessions, security, allowed list).
    -   `ParkingSystem.py`: Core logic, TinyDB storage, allowed-car enforcement.
    -   `ANPR/`: License plate recognition.
    -   `APSD/`: Parking spot detection and analyzer.
    -   `SceneController.py`: Demo scene runner for scripted entry/exit flows.
-   **Dashboard (Next.js, Tailwind)**
    -   `dashboard/app/page.tsx`: Live lot view (grid, stats, gate status, scene triggers, media).
    -   `dashboard/app/allowed/page.tsx`: Manage allowed plates.
    -   `dashboard/app/find-car/page.tsx`: Lookup latest spot/status by plate.

## Features

-   Automatic number plate recognition at gate.
-   Parking spot detection and assignment.
-   Whitelist/blacklist (allowed cars) with security toggle.
-   Scene simulator to demo entry/exit flows with media previews.
-   Live dashboard: parking grid, gate timeline, scene triggers, before/after images.
-   Allowed list management UI and “Find Car” lookup (latest session + spot).

## Backend setup (Python)

1.  Create/activate venv:
    
    ```bash
    python3 -m venv venvsource venv/bin/activate
    ```
    
2.  Install deps:
    
    ```bash
    pip install -r requirements.txt
    ```
    
3.  Run API:
    
    ```bash
    python app.py
    ```
    
    -   Default port: `5001`
    -   Data: `parking_sessions.json` (TinyDB)
    -   Models: APSD weights path `./APSD/apsd.pt` (configured in `ParkingSystem.py`).

Key endpoints (sample):

-   `POST /event/entry|scan|exit`
-   `POST /scene/<id>` (demo scenes)
-   `GET /sessions/plate/<plate>/latest`
-   Allowed list: `GET /allowed/list`, `POST /allowed/add`, `POST /allowed/remove`

## Frontend setup (Next.js dashboard)

1.  From `dashboard/`:
    
    ```bash
    npm install
    ```
    
2.  Run dev server:
    
    ```bash
    npm run dev
    ```
    
3.  Point the dashboard to the backend (optional):
    -   Set `NEXT_PUBLIC_API_BASE` (defaults to `http://localhost:5001`).

Routes:

-   `/` — live lot dashboard.
-   `/allowed` — whitelist management.
-   `/find-car` — plate lookup (latest session + spot).

Assets:

-   Scene images expected under `dashboard/public/img` (car1.jpeg, car2.jpeg, park0.png, park1.png, park2.png).

## Notes

-   Plate normalization: plates are slugged to lowercase with dashes (`slug_plate`).
-   `parking_sessions.json` keeps sessions and allowed cars; if you change storage, update `ParkingSystem.py`.
-   Gate states and delays are set in `dashboard/app/constant.ts` (mirrors `constant.py`).