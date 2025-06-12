# Lead Generation Tool

This project consists of a Python-based backend (FastAPI) and a React/TypeScript frontend (Vite) designed for lead generation, analytics, and CRM integration.

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Running the Application](#running-the-application)
  - [Starting the Backend](#starting-the-backend)
  - [Starting the Frontend](#starting-the-frontend)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Lead Search & Scraping:** Search and scrape business leads from various sources.
- **Lead Enrichment:** Enrich lead data with additional information (e.g., news, contact details).
- **Analytics Dashboard:** Visualize lead distribution, projections, and top leads.
- **CRM Integration:** Simulate or integrate with CRM systems for lead management.
- **AI-Powered Insights:** Generate insights using Gemini models.

## Project Structure
```
Intern Project/
  backend/
    app/
      api/             # FastAPI endpoints
      crm/             # CRM integration logic
      models/          # Pydantic models for data validation
      services/        # Business logic and external API integrations (ML, Scraping, Enrichment, Leads)
    venv/            # Python virtual environment
    requirements.txt # Python dependencies
  frontend/
    public/          # Static assets
    src/
      assets/        # Frontend assets
      pages/         # React pages (e.g., AnalyticsPage, LoginPage)
      services/      # Frontend API calls and services
    node_modules/    # Node.js dependencies
    package.json     # Frontend dependencies and scripts
    vite.config.ts   # Vite configuration
  README.md          # Project README
  .gitignore         # Git ignore file for the root
```

## Prerequisites
Before you begin, ensure you have the following installed:
- Git
- Python 3.9+
- Node.js (LTS version recommended)
- npm (Node Package Manager)
- MongoDB (running locally or accessible via a URI)

## Setup Instructions

### Backend Setup
1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
2.  **Create a Python virtual environment (if you haven't already):**
    ```bash
    python3 -m venv venv
    ```
3.  **Activate the virtual environment:**
    -   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
    -   **Windows (Command Prompt):**
        ```bash
        venv\Scripts\activate.bat
        ```
    -   **Windows (PowerShell):**
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
4.  **Install backend dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Frontend Setup
1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```
2.  **Install frontend dependencies:**
    ```bash
    npm install
    ```

## Running the Application

### Starting the Backend
1.  **Ensure you are in the `backend` directory and your virtual environment is activated.**
2.  **Run the FastAPI application:**
    ```bash
    python -m uvicorn app.main:app --reload
    ```
    The backend server should start on `http://localhost:8000`.

### Starting the Frontend
1.  **Ensure you are in the `frontend` directory.**
2.  **Start the Vite development server:**
    ```bash
    npm run dev
    ```
    The frontend application should open in your browser, typically at `http://localhost:5173` (or `http://localhost:5174` if 5173 is in use).

## Environment Variables
Both the backend and frontend require environment variables for configuration.
-   **Backend:** Create a `.env` file in the `backend/` directory based on `backend/.env.example`.
-   **Frontend:** Create a `.env` file in the `frontend/` directory based on `frontend/.env.example`.

**Important:** Never commit your actual `.env` files to Git. Only the `.env.example` files should be tracked.

Fill in the necessary API keys and configurations in your `.env` files.

## Usage
Once both the backend and frontend servers are running, open your web browser and navigate to the frontend URL (e.g., `http://localhost:5173`).

-   You should see the login page.
-   After logging in, you can use the dashboard to search for companies, view analytics, generate insights, and manage leads.

## Troubleshooting
-   **Port in use error:** If you encounter an "Address already in use" error when starting a server, kill the process using that port.
    -   **Linux/macOS:** `lsof -ti:<PORT> | xargs kill -9` (replace `<PORT>` with `8000` or `5173`)
    -   **Windows:** Find the PID using `netstat -ano | findstr :<PORT>` and then kill it with `taskkill /PID <PID> /F`
-   **CORS errors:** Ensure `http://localhost:5173` (or the port your frontend is running on) is allowed in your backend's CORS configuration (in `backend/app/main.py`).
-   **API Key issues:** Double-check that all required API keys are correctly set in your `.env` files.
-   **MongoDB connection:** Ensure your MongoDB instance is running and accessible at the URI specified in your `backend/.env` file.

## Contributing
If you'd like to contribute to this project, please follow these steps:
1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and ensure tests pass.
4.  Commit your changes with a clear message.
5.  Push your branch and open a pull request.

## License
[Specify your project's license here, e.g., MIT, Apache 2.0, etc.] 