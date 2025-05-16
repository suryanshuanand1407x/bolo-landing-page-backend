# Bolo Landing Page Backend

This is the backend service for the Bolo landing page, built with FastAPI and Supabase.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- A Supabase account and project

## Local Development Setup

1. Clone the repository and navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   cd api
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the `api` directory with your Supabase credentials:
   ```env
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
   ```

   You can find these credentials in your Supabase project dashboard under Project Settings > API.

5. Start the development server:
   ```bash
   python3 run.py
   ```

   The server will start at `http://localhost:8000`

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Available Endpoints

- `GET /health` - Health check endpoint
- `POST /api/waitlist` - Add email to waitlist
- `GET /api/waitlist` - Get all waitlist entries
- `POST /api/contact` - Submit contact form
- `GET /api/contact` - Get all contact form submissions

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | Your Supabase service role key |
| `PORT` | Port number for the server (default: 8000) |