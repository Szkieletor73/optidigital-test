# Backend API

Simple FastAPI backend for the project.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- http://localhost:8000 - Root endpoint
- http://localhost:8000/health - Health check
- http://localhost:8000/api/hello - Sample API endpoint
- http://localhost:8000/docs - Interactive API documentation

## CORS Configuration

The backend is configured to accept requests from the Vue frontend running on `http://localhost:5173`.