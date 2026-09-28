# DSL — Bridging the Humanitarian Funding Gap

> A decision-intelligence platform that identifies forgotten humanitarian crises by exposing the mismatch between crisis severity and donor funding.

**3rd place out of 24 projects at Georgia Tech Hacklytics' Databricks Challenge.**

DSL helps humanitarian advocates move from fragmented crisis data to an actionable funding story. It combines humanitarian needs and funding data, highlights crises that are both severe and underfunded, and produces lightweight Crisis Alerts that can be shared even in low-bandwidth environments.

![DSL landing page](DSLFrontend/public/landing-1.png)

## Why we built it

During a conversation with Mary, a United Nations representative, we learned that crises are not overlooked only because funding is limited. They are also overlooked because the data needed to explain their urgency is scattered across different systems.

A country may have millions of people in need and a high severity score while receiving little funding—or no new funding momentum at all. Traditional dashboards show individual figures, but they do not always reveal this structural mismatch. DSL was built to flag those neglect zones automatically and help advocates turn the evidence into a clear, defensible funding ask.

## What DSL does

- **Interactive crisis map:** Explore humanitarian conditions geographically and open country-level details.
- **Underfunded-crisis ranking:** Compare the least-funded crises across 2023, 2024, and 2025.
- **Red Flag analysis:** Highlights crises with a severity score of at least `4.0` and funding coverage below `25%`.
- **Structural Gap:** Calculates the difference between people in need and people targeted for assistance.
- **Funding Velocity:** Measures year-over-year movement in total humanitarian funding.
- **Severity–funding mismatch view:** Uses a quadrant-based scatter plot to make high-severity, low-funding emergencies immediately visible.
- **Natural-language analysis:** Sends humanitarian questions to a Databricks Genie Space and returns data-backed answers and visualizations.
- **Country drill-downs:** Surfaces people in need, people targeted, requirements, funding, and response-plan details.
- **Low-bandwidth Crisis Alerts:** Exports the most underfunded emergencies as compact Markdown or CSV files.
- **Resilient demo mode:** Falls back to bundled crisis data when the live Databricks connection is unavailable.

## Decision-intelligence logic

DSL converts raw humanitarian indicators into decision-ready signals:

| Signal | Calculation or rule | Why it matters |
| --- | --- | --- |
| Funding coverage | `funding / requirements` | Shows how much of an appeal has been funded |
| Funding gap | `requirements - funding` | Shows the remaining monetary need |
| Structural gap | `people in need - people targeted` | Finds people whose needs are recognized but who are not included in the response target |
| Funding per person | `funding / people in need` | Makes funding comparable across crises of different sizes |
| Funding velocity | Year-over-year change in total funding | Reveals whether donor support is accelerating or stalling |
| Red Flag | `severity >= 4.0` and `funding coverage < 25%` | Identifies severe crises at greatest risk of neglect |

The application also uses a severity proxy when live severity data is not available, combining funding shortfall and relative population in need. This keeps the decision view useful in fallback mode while clearly separating derived signals from source data.

## Architecture

```text
Humanitarian datasets
        │
        ▼
Databricks Lakehouse + Unity Catalog
        │
        ├── SQL Warehouse ──► Express API ──► React dashboard
        │
        └── Genie Space ────► Natural-language analysis
                                  │
                                  ▼
                   Maps, rankings, alerts, and exports
```

### Technology stack

- **Frontend:** React 19, Vite, Tailwind CSS, Recharts, Mapbox GL, GSAP
- **Application API:** Node.js, Express, Databricks SQL Statement Execution API, Databricks Genie API
- **Data and AI:** Databricks SQL Warehouse, Unity Catalog, Genie Space
- **Supporting data service:** FastAPI, pandas, OpenAI

## Run locally

### Prerequisites

- Node.js 18 or later
- npm
- A Databricks workspace, SQL Warehouse, personal access token, and crisis-data table for live data
- A Mapbox access token for the interactive map

### 1. Install the frontend

```bash
cd DSLFrontend
npm install
```

### 2. Configure environment variables

Create `DSLFrontend/.env`:

```env
DATABRICKS_PAT=your_databricks_personal_access_token
DATABRICKS_SERVER_HOSTNAME=your-workspace.cloud.databricks.com
DATABRICKS_WAREHOUSE_ID=your_sql_warehouse_id
DATABRICKS_TOP_CRISES_TABLE=your_catalog.your_schema.your_table
GENIE_SPACE_ID=your_genie_space_id
VITE_MAPBOX_ACCESS_TOKEN=your_mapbox_access_token
```

The Databricks table should contain the fields used by the dashboard, including:

```text
country, country_iso3, year, people_in_need, people_targeted,
requirements, funding, coverage_ratio, funding_gap
```

Use a Serverless SQL Warehouse and ensure the token's principal has permission to use the warehouse and select from the configured table.

### 3. Start the dashboard and API

```bash
npm run dev:all
```

Open the Vite URL shown in the terminal, normally [http://localhost:5173](http://localhost:5173). The Express API runs on [http://localhost:3001](http://localhost:3001).

If Databricks is not configured or cannot be reached, the dashboard continues with the bundled static dataset. Live Genie questions and server-generated exports require valid Databricks credentials.

### Other commands

```bash
npm run dev       # Frontend only
npm run server    # Databricks API only
npm run build     # Production build
npm run lint      # ESLint checks
npm run preview   # Preview a production build
```

## API overview

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/api/health` | Check API and Databricks configuration status |
| `GET` | `/api/top_crises` | Retrieve crisis records from Databricks |
| `GET` | `/api/mismatch` | Build severity-versus-funding points and Red Flags |
| `GET` | `/api/decision-metrics` | Return severity gap, structural gap, and funding velocity |
| `GET` | `/api/crisis-alert` | Download a low-bandwidth Markdown or CSV alert |
| `POST` | `/api/chat` | Run guarded natural-language humanitarian queries |
| `GET` | `/api/genie/status` | Check Genie configuration |
| `POST` | `/api/genie/ask` | Ask the configured Databricks Genie Space a question |

More Databricks troubleshooting notes are available in [`DSLFrontend/server/README-DATABRICKS.md`](DSLFrontend/server/README-DATABRICKS.md).

## Challenges we overcame

- **The owner-access paradox:** Databricks authentication and registration identifiers required re-synchronizing Azure Entra ID permissions.
- **Visualizing the invisible:** Low funding can look less urgent than high severity, so we created a derived neglect signal and a quadrant view that displays both dimensions together.
- **Real-time API reliability:** We addressed HTML responses and `Unexpected token '<'` errors by validating API payloads, keeping the SQL Warehouse ready, and providing a local-data fallback.
- **Trustworthy AI output:** The Genie Space was given explicit schema instructions and humanitarian guardrails so answers remain grounded in the available statistics.

## What we are proud of

- Translating a UN representative's desired metrics—especially Funding Velocity and structural mismatch—into working analytical logic.
- Turning a complex humanitarian dataset into an advocacy tool that can surface neglected crises in seconds.
- Generating compact Crisis Alerts for field officers and partners with limited connectivity.
- Achieving a 100% benchmark on the Genie Space instructions used to keep responses grounded in humanitarian data.
- Placing **3rd out of 24 projects** in the Georgia Tech Hacklytics Databricks Challenge.

## What we learned

In humanitarian work, clarity can matter more than complexity. A concise Markdown table that reaches the right donor at the right moment may be more useful than a polished 50-page report that arrives too late.

## What's next

- **Media sentiment integration:** Compare GDELT media attention with funding coverage to identify truly forgotten crises.
- **Predictive alerts:** Forecast a funding stall before deteriorating support compounds a crisis.
- **Richer benchmarking:** Compare similar crisis types across regions to make funding requests more defensible.
- **Automated delivery:** Distribute Crisis Alerts through email, messaging, and field-friendly offline channels.

## Repository structure

```text
DSL-Hackathon/
├── DSLFrontend/   # React dashboard and Databricks/Genie Express API
└── DSLBackend/    # FastAPI and pandas-based supporting analysis service
```

---

Built for the Georgia Tech Hacklytics Databricks Challenge to help humanitarian decision-makers find the crises the world is at risk of forgetting.
