# Lead Generation Tool

This project consists of a Python-based backend (FastAPI) and a React/TypeScript frontend (Vite) designed for lead generation, analytics, and CRM integration.

## Table of Contents
- [Author](#author)
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
- [Technical Deep Dive](#technical-deep-dive)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Author
Dhavala Kartikeya Somayaji

## Features
- **Lead Search & Scraping:** Efficiently search and scrape business leads from various sources. This feature ensures a comprehensive database of potential clients.
- **Lead Enrichment:** Enhance raw lead data by integrating with external APIs to fetch additional information like company news, contact details, and industry-specific metrics.
- **Analytics Dashboard:** A dynamic dashboard visualizing key lead metrics, including lead distribution by industry/location, lead projections, and identification of top-performing leads, providing actionable insights for sales strategies.
- **CRM Integration:** Seamlessly simulate or integrate with CRM systems to manage the lead lifecycle, track interactions, and streamline sales processes.
- **AI-Powered Insights (Unique Feature):** A distinctive "Insights" module that leverages advanced ML models (Gemini) to analyze company data and provide comprehensive pros and cons, helping customers make informed decisions about potential leads.
- **Real-time Updates (WebSockets):** (If applicable, describe where WebSockets are used for real-time updates, e.g., for lead scraping progress, analytics updates)
- **Data Deduplication:** Robust mechanisms are implemented to identify and eliminate duplicate leads, ensuring data integrity and preventing redundancy in the system.

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

## Technical Deep Dive

### ML Integration for Lead Enhancement
The backend integrates with machine learning models (specifically Gemini) to analyze lead data and provide actionable insights. This involves:
-   **Data Processing:** Raw lead data is processed and fed into the ML models.
-   **Insight Generation:** The models generate a structured output, including identified pros and cons for each company, enhancing the value proposition for sales teams.
-   **Model Management:** (If applicable, describe how models are loaded, updated, or fine-tuned. E.g., models are loaded on application startup for efficiency.)

### CRM Integration
The CRM integration allows for seamless management of leads. This is primarily handled within the `backend/app/crm/` and `backend/app/services/crm_service.py` modules. Key aspects include:
-   **Lead Status Management:** Leads can be moved through different stages (e.g., New, Contacted, Qualified) to reflect their progress in the sales pipeline.
-   **Data Synchronization:** (If applicable, mention if there's any data synchronization with a real CRM or if it's a simulated environment). The current implementation simulates sending lead data to a CRM, allowing for flexible integration with various platforms.

### Analytics Dashboard
The analytics dashboard provides a comprehensive overview of lead performance, powered by data fetched from MongoDB and processed by the ML service. It visualizes:
-   **Lead Distribution:** Charts showing the distribution of leads across different industries, locations, or other relevant categories.
-   **Lead Projections:** (If applicable, describe how lead projections are calculated or displayed).
-   **Top Leads:** Identification and display of high-potential leads based on predefined criteria or ML-driven scoring.

### Data Deduplication
To maintain data cleanliness and efficiency, the application incorporates a deduplication mechanism. This ensures that:
-   New leads are checked against existing records to prevent duplicates.
-   Deduplication logic is applied during (e.g., data ingestion or before saving to MongoDB) to maintain a unique and high-quality lead database.

### MongoDB Integration
MongoDB serves as the primary NoSQL database for storing lead information. Key aspects of its integration include:
-   **Flexible Schema:** MongoDB's flexible schema is ideal for storing diverse lead data, which may vary depending on the scraping source or enrichment process.
-   **Efficient Data Retrieval:** Indexes are utilized for quick retrieval of leads based on various search criteria.
-   **Scalability:** MongoDB's architecture supports scaling to handle growing volumes of lead data.

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