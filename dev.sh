#!/bin/bash

# AgentDesk – Local Development Launcher
# This script starts both the FastAPI backend and Next.js frontend concurrently.

# Set up colors for logging
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting AgentDesk Stack...${NC}"

# Ensure we are in the project root
PROJECT_ROOT=$(pwd)

# Function to kill background processes on exit
cleanup() {
    echo -e "\n${BLUE}🛑 Shutting down servers...${NC}"
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit
}

# Trap SIGINT (Ctrl+C) and call the cleanup function
trap cleanup SIGINT

# 1. Start Backend (FastAPI)
echo -e "${GREEN}📡 Starting Backend (FastAPI) on port 8000...${NC}"
source venv/bin/activate
cd "$PROJECT_ROOT/backend"
uvicorn main:app --port 8000 &
BACKEND_PID=$!

# 2. Start Frontend (Next.js)
echo -e "${GREEN}💻 Starting Frontend (Next.js) on port 3000...${NC}"
cd "$PROJECT_ROOT/frontend"
# Ensure /opt/homebrew/bin is in path for Node/npm
export PATH="/opt/homebrew/bin:$PATH"
npm run dev &
FRONTEND_PID=$!

echo -e "${BLUE}✅ Both servers are starting up!${NC}"
echo -e "${BLUE}🔗 Backend: http://localhost:8000${NC}"
echo -e "${BLUE}🔗 Frontend: http://localhost:3000${NC}"
echo -e "${BLUE}💡 Press Ctrl+C to stop both servers at any time.${NC}"

# Wait for background processes to keep the script alive
wait
