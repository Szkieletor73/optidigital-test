# Docker Deployment Guide

This project supports Docker deployment with separate containers for the frontend and backend.

## Quick Start

### Production Deployment

1. **Build and start all services:**
   ```bash
   npm run docker:build
   npm run docker:up
   ```

2. **Access the application:**
   - Frontend: http://localhost
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Development with Docker

1. **Start development environment:**
   ```bash
   npm run docker:dev
   ```

2. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000

## Manual Docker Commands

### Build Images
```bash
# Build backend
docker build -f Dockerfile.backend -t optidigital-backend .

# Build frontend
docker build -f Dockerfile.frontend -t optidigital-frontend .
```

### Run Containers
```bash
# Run backend
docker run -d -p 8000:8000 --name backend optidigital-backend

# Run frontend (depends on backend)
docker run -d -p 80:80 --name frontend --link backend optidigital-frontend
```

## Environment Configuration

The application uses different API endpoints based on the environment:

- **Development**: `http://localhost:8000`
- **Production**: `/api` (proxied through nginx to backend container)

## Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │
│   (nginx:80)    │────│   (FastAPI:8000)│
│   Vue.js + Vite │    │   Python        │
└─────────────────┘    └─────────────────┘
```

### Frontend Container
- **Base**: nginx:alpine
- **Port**: 80
- **Features**: 
  - Serves built Vue.js application
  - Proxies `/api/*` requests to backend
  - Handles client-side routing

### Backend Container
- **Base**: python:3.11-slim
- **Port**: 8000
- **Features**:
  - FastAPI application
  - Authentication endpoints
  - API documentation at `/docs`

## Useful Commands

```bash
# View logs
npm run docker:logs

# Stop all services
npm run docker:down

# Rebuild and restart
npm run docker:build && npm run docker:up

# Access container shell
docker exec -it optidigital-backend bash
docker exec -it optidigital-frontend sh
```

## Troubleshooting

### Common Issues

1. **Port conflicts**: Make sure ports 80 and 8000 are available
2. **Build failures**: Check Docker daemon is running
3. **API connection issues**: Verify backend container is healthy

### Health Checks

The backend container includes a health check that verifies the API is responding:

```bash
# Check container health
docker ps
# Look for "healthy" status
```

### Environment Variables

Create `.env` file for custom configuration:

```bash
# Frontend
VITE_API_BASE_URL=http://your-backend-url

# Backend (if needed)
DATABASE_URL=your-database-url
SECRET_KEY=your-secret-key
```