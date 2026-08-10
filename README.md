# Sentinels of Truth

## AI Fact Verification System

Sentinels of Truth is a web-based fact verification system that accepts a news claim from a user, investigates the claim using external search and an AI model, generates a verification report, and manages the resulting information using a database.

The system is designed around a multi-agent workflow:

- **Agent Alpha – Investigator:** investigates the submitted claim using search and an AI model.
- **Agent Beta – Archivist:** processes the verification result and decides how the information should be handled in the database.

The application consists of a FastAPI backend and a simple HTML/CSS/JavaScript frontend.

---

## Features

- Submit a news claim through a web interface.
- Verify claims using an AI-powered investigation workflow.
- Search for supporting information and evidence.
- Generate a verdict and confidence score.
- Display a summary and sources.
- Maintain verification information in a SQLite database.
- Show the database action and workflow history.
- Separate frontend and backend components.

---

## Project Structure

```text
assignment/
│
├── backend/
│   ├── agents/
│   │   ├── alpha.py
│   │   └── beta.py
│   │
│   ├── config/
│   │   └── llm.py
│   │
│   ├── database/
│   │   ├── crud.py
│   │   ├── db.py
│   │   ├── dependencies.py
│   │   └── models.py
│   │
│   ├── graph/
│   │   ├── state.py
│   │   └── workflow.py
│   │
│   ├── tools/
│   │   └── search.py
│   │
│   ├── main.py
│   ├── schemas.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── .gitignore
└── README.md
```

---

## Technology Stack

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- SQLite

### AI / Agents

- Google Gemini API
- LangGraph

### Frontend

- HTML
- CSS
- JavaScript

---

## System Flow

The basic flow of the application is:

```text
User
 │
 │ enters a claim
 ▼
Frontend
 │
 │ POST /verify
 ▼
FastAPI Backend
 │
 ▼
LangGraph Workflow
 │
 ├──► Agent Alpha
 │       │
 │       ├── Investigates claim
 │       ├── Uses search
 │       └── Uses AI model
 │
 ▼
Agent Beta
 │
 ├── Processes verification result
 └── Determines database action
 │
 ▼
SQLite Database
 │
 ▼
Verification Response
 │
 ▼
Frontend
 │
 ▼
User sees result
```

---

## Installation

### Requirements

- Python 3.10 or newer
- Internet connection
- A Google Gemini API key

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd assignment
```

### 2. Create a virtual environment

From the project root:

**Windows**

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, the backend can also be run using the Python executable inside the environment directly.

### 3. Install backend dependencies

```powershell
pip install -r backend/requirements.txt
```

---

## Configuration

The application requires an API key for the AI model.

Inside the backend directory, create:

```text
backend/.env
```

Add:

```env
GOOGLE_API_KEY=your_actual_api_key
```

Replace the placeholder with your own API key.

### Security

Do not commit the `.env` file to GitHub. The repository contains `.env.example` as a template. Users should create their own `.env` file locally using `.env.example` as a reference.

---

## Running the Backend

Open a terminal and navigate to the backend:

```powershell
cd backend
```

Activate the virtual environment if necessary:

```powershell
..\venv\Scripts\Activate.ps1
```

Start FastAPI:

```powershell
python -m uvicorn main:app --reload
```

The backend will normally be available at:

```text
http://127.0.0.1:8000
```

FastAPI's interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

## Running the Frontend

Open a second terminal and navigate to the frontend directory:

```powershell
cd frontend
```

Start a simple local HTTP server:

```powershell
python -m http.server 5500
```

Open the frontend in a browser:

```text
http://127.0.0.1:5500
```

---

## Using the Application

1. Start the backend.
2. Start the frontend.
3. Open the frontend in a browser.
4. Enter a news claim.
5. Click **Verify Claim**.
6. Wait for the verification result.
7. Review:
   - Claim
   - Verdict
   - Confidence
   - Summary
   - Sources
   - Database action
   - Workflow history

---

## API

### Health Check

**Request**

```http
GET /
```

**Example**

```text
http://127.0.0.1:8000/
```

### Verify Claim

**Request**

```http
POST /verify
```

**Request body**

```json
{
    "claim": "The Earth revolves around the Sun."
}
```

The endpoint processes the claim through the verification workflow and returns the verification result.

---

## Database

The application uses SQLite for local persistent storage. The database is created by the backend according to the SQLAlchemy models. The database is intentionally excluded from the Git repository because it is generated locally and may contain runtime data.

---

## Agents

### Agent Alpha – Investigator

Agent Alpha is responsible for investigating the submitted claim. Its responsibilities include:

1. Receiving the claim.
2. Identifying information needed for verification.
3. Searching for relevant information.
4. Using the AI model to analyze the available evidence.
5. Producing a verification report.

### Agent Beta – Archivist

Agent Beta is responsible for managing the long-term information stored by the system. It receives the verification report from Agent Alpha and determines the appropriate database action. This separates investigation from database management.

---

## Workflow

The agents are connected through a LangGraph workflow. The simplified workflow is:

```text
START
  │
  ▼
Investigator
  │
  ▼
Archivist
  │
  ▼
END
```

The workflow passes the claim and verification information between the agents using the application state.

---

## Testing

The project contains component-level test scripts that can be used to verify individual parts of the system. Examples include testing:

- AI model connectivity
- Search functionality
- Agent Alpha
- Graph workflow

The application can also be tested through the frontend by submitting different claims.

---

## Example Claims

Example claims that can be used for testing include:

```text
The Earth revolves around the Sun.
```

```text
India landed humans on Mars.
```

The exact verdict returned by the application depends on the verification workflow and the evidence available at runtime.

---

## Troubleshooting

### Backend does not start

Make sure the virtual environment is active and dependencies are installed:

```powershell
pip install -r backend/requirements.txt
```

Then:

```powershell
cd backend
python -m uvicorn main:app --reload
```

### API key error

Check that `backend/.env` exists and contains:

```env
GOOGLE_API_KEY=your_actual_api_key
```

Make sure the API key is valid.

### Frontend cannot connect to backend

Make sure the backend is running first:

```text
http://127.0.0.1:8000
```

Then start the frontend:

```powershell
python -m http.server 5500
```

---

## Security Note

API keys and other secrets should never be committed to the repository. The `.gitignore` file excludes environment files containing secrets. Users should create their own `.env` file locally using `.env.example` as a reference.

---

## License

This project was developed as part of an assessment/project exercise.
