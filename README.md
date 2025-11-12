# WHACK25 — Financial Literacy & Contract Analyzer

> An interactive web app that combines gamified learning, personal finance tracking, and contract analysis (LLM-powered) to help users improve financial literacy, credit health, and make safer signing decisions.

---

## Table of contents

* [Project overview](#project-overview)
* [Key features](#key-features)
* [Architecture & repository layout](#architecture--repository-layout)
* [Prerequisites](#prerequisites)
* [Quick start (development)](#quick-start-development)
* [Database setup & maintenance](#database-setup--maintenance)
* [Contract analysis (LLM / Gemini)](#contract-analysis-llm--gemini)
* [PDF highlighting & contract review pipeline](#pdf-highlighting--contract-review-pipeline)
* [Frontend details](#frontend-details)
* [Security, privacy & compliance notes](#security-privacy--compliance-notes)
* [Testing & quality assurance](#testing--quality-assurance)
* [Deployment recommendations](#deployment-recommendations)
* [Roadmap & suggested improvements](#roadmap--suggested-improvements)
* [Contributing](#contributing)
* [Credits & acknowledgements](#credits--acknowledgements)
* [License](#license)

---

## Project overview

WHACK25 is a full-stack prototype that teaches and nudges better financial behaviour through three integrated features:

1. **Gamified credit-skill learning (Snake game)** — Players collect positive items that *improve* a simulated credit score and avoid negative items that *damage* it. When an item is collected, an explanation box appears that teaches *why* the user gained or lost points.

2. **Personal financial tracker** — A lightweight income/expense tracker where users can create records, view them in a table, filter by date ranges, and visualise their finances using graphs.

3. **Contract analysis and PDF highlighting (LLM-powered)** — Users upload a contract (PDF). The app analyses the contract using a large language model, returns a percentage score that indicates how beneficial the contract is to the user, lists suggested improvements, and renders the original PDF with the "risky" or unfavourable passages highlighted for quick review.

These components are stitched together in a single app repository that contains both backend logic, LLM integration, PDF tooling, and front-end assets.

---

## Key features (expanded)

### 1) Snake — gamified credit education

* Collect `positive` items that increase a simulated credit score and show a short educational pop-up explaining the credit principle.
* Collecting `negative` items reduces the score and shows corrective guidance.
* Purpose: teach cause-and-effect (e.g., on-time payments, credit utilisation, missed payments).

### 2) Financial tracker

* Create, edit, and delete income & expense entries.
* Table view with currency and timestamp information.
* Chart visualisations (time-series / pie / bar) to present spending vs income.
* Filtering controls to focus the view on date ranges or categories.

### 3) Contract analysis (LLM-driven)

* Upload PDF contracts.
* The LLM (project uses *Gemini 2.5 Pro* via an integration module) analyses the contract and:

  * Produces an overall numeric score (how favourable the contract is to the user).
  * Lists a prioritized set of issues and recommended changes.
  * Highlights clauses in the PDF that are unfavourable or require attention.
* This feature is intended to act as a *consultant-style assistant* rather than a legally binding opinion; results should encourage professional legal review for high-risk contracts.

---

## Architecture & repository layout

(High level — file names and intended purpose)

* `app.py` — Main Python web application entry point (starts the Flask app and registers routes / API endpoints).
* `gemini.py` — LLM integration module (encapsulates prompt engineering and calls to the Gemini 2.5 Pro model).
* `pdfHighlighting.py` — PDF parsing and highlighting utilities (reads PDFs, maps text spans to pages, writes annotated PDFs).
* `databaseSetup.py` — Creates the local database schema and seeds any initial data.
* `databaseDelete.py` — Utility to remove or reset database state.
* `database.db` — Local SQLite database file (example/dev DB checked into repo).
* `requirements.txt` — Python dependencies.

Frontend / static assets:

* `index_4.html` — Primary HTML file / single-page app entry (likely contains the UI for the three features or bootstraps the front-end).
* `script.js` — Front-end logic (game implementation, charts, AJAX calls to the backend).
* `signup.js` — Signup / authentication related client logic.
* `style.css` — Styling for the UI.

Node / auxiliary server:

* `server.js` — Optional Node server (used for static hosting, socket connections, or auxiliary realtime features).

Uploads / runtime data:

* `uploads/` — Folder for user-uploaded PDFs and images.

> Note: This layout and file-role mapping was confirmed by inspecting the repository file listing. For the authoritative source, see the project on GitHub.

---

## Prerequisites

* **Python 3.10+** (recommended). Ensure `python` and `pip` are available.
* A Google Cloud account / environment or other mechanism to call Gemini 2.5 Pro (the repository contains `gemini.py` for that integration). You must supply API credentials as environment variables (see below).
* Browser for the front-end.
* Optional: `node` / `npm` if you use `server.js` locally.

---

## Quick start (development)

1. Clone the repository:

```bash
git clone https://github.com/Joshua-Cullen/WHACK25.git
cd WHACK25
```

2. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
```

3. Install Python requirements:

```bash
pip install -r requirements.txt
```

4. Set environment variables (example `.env` / export):

```
# Example environment variables used by the app
GEMINI_API_KEY="<YOUR_GEMINI_KEY>"
GEMINI_MODEL="gemini-2.5-pro"
FLASK_ENV=development
SECRET_KEY="a-strong-secret-for-session"
```

5. Prepare the database:

```bash
python databaseSetup.py
```

6. Run the application (simple):

```bash
python app.py
```

Visit `http://127.0.0.1:5000` (or the port printed by the app).

If the project uses `server.js` for additional features, run:

```bash
node server.js
```

---

## Database setup & maintenance

* `databaseSetup.py` creates the required tables and any example rows — run it before launching the app in a fresh environment.
* `databaseDelete.py` wipes or resets the database when you want to clear dev data — **use with care** (backup DB first).
* The project contains `database.db` as a development database. **Do not** use a committed DB in production — replace with a managed DB or remove the file from version control.

---

## Contract analysis (LLM / Gemini)

**Important:** Contract review processes may handle sensitive PII. The repository contains `gemini.py` that encapsulates prompt engineering and the calls to the model. Basic guidance:

* Do not commit API keys or secrets to the repository. Use environment variables or a secrets manager.
* Add throttling and rate-limits when calling the LLM to avoid runaway costs.
* Keep prompt templates in a separate file or in a secure config so you can iterate on them without changing code.
* Sanitize or redact PII from the contract before sending it to any external LLM if you need to comply with strict data policies.

Typical flow (existing repo suggests this):

1. User uploads PDF contract via frontend.
2. Backend extracts text (page-by-page) and sends the relevant text with a structured prompt to `gemini.py`.
3. The LLM returns:

   * An overall percentage score (benefit to user).
   * A ranked list of concerns with justifications and suggested rephrasing.
4. Backend maps the LLM-identified spans back to PDF coordinates and uses `pdfHighlighting.py` to create an annotated PDF for the user to download/view.

---

## PDF highlighting & contract review pipeline

`pdfHighlighting.py` contains utilities to parse PDFs and annotate pages. For robust PDF processing in production, consider:

* Using reliable libraries such as `PyMuPDF` (fitz), `pdfminer.six`, or `pypdf`/`PyPDF2` for extraction.
* Mapping text offsets to page coordinates is non-trivial — unit tests are recommended for the mapping logic.
* Respect file-size limits and scan uploads for malware.

---

## Frontend details

* `index_4.html` is the main static UI — open it directly for a quick demo or use the bundled Flask app for a fully integrated experience.
* `script.js` contains game logic (snake), charting and AJAX calls. The snake game should trigger a modal/pop-up after the snake eats items to explain credit impacts.
* Charting libraries: if the project uses charting (e.g., Chart.js, or Plotly), ensure the dependency is declared in `requirements.txt` or in a `package.json` if the JS libs are installed via npm.
* `signup.js` indicates there is some signup/auth UI; verify that password hashing and session handling occur server-side (do not trust client-side-only auth).

---

## Security, privacy & compliance notes

Because the app handles financial data and contract documents, treat the project as potentially sensitive:

* **Secrets**: Store LLM API keys, DB credentials, and other secrets in environment variables or secret managers. Add `.env` to `.gitignore`.
* **Access control**: Implement server-side authentication, session management, and ACLs for uploaded contracts.
* **Encryption**: Encrypt sensitive data at rest and in transit (TLS for web traffic; consider encrypting files stored in `uploads/`).
* **Data retention policy**: Define how long you will keep uploaded contracts and financial records; provide a deletion mechanism.
* **Logging**: Mask or redact PII in logs.
* **Legal**: Display a clear disclaimer that the contract analysis is AI-assisted and not a substitute for professional legal advice.

---

## Testing & quality assurance

* Add unit tests for:

  * PDF text-to-coordinate mappings.
  * LLM prompt templates and result parsing code (ensure predictable parsing for the expected JSON structure).
  * Financial tracker CRUD functions and date-range filtering.
* Add integration tests for upload → analysis → highlighted PDF end-to-end.

---

## Deployment recommendations

* Containerise the application (Dockerfile) so you can deploy consistently. A multi-stage image with a small runtime image is recommended.
* Use managed services for the DB in production (Postgres/RDS/Cloud SQL) instead of local SQLite.
* Protect endpoints using HTTPS, API gateway (rate limiting), and authenticated access to the contract analysis features (to reduce cost and exposure).
* For LLM calls (Gemini), consider deploying proxy services that introduce caching and cost-control features.

---

## Roadmap & suggested improvements

1. Harden authentication: server-side password hashing (bcrypt/argon2), account recovery, email verification.
2. Add RBAC for multi-user organisations.
3. Move from SQLite to Postgres for production.
4. Add a usage/cost dashboard for LLM calls and page-level audit logs.
5. Internationalisation: multi-currency and multi-language contract support.
6. Automated unit & integration test coverage.
7. CI pipeline with linting and security checks.

---

<!-- End of README -->
