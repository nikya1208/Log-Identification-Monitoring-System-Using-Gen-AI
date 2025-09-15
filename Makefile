# Makefile for simplifying Docker, linting, and deployment commands

# Environment Variables
ENV_FILE = .env
DOCKER_COMPOSE = docker-compose -f docker-compose.yml

# Run Backend
run-backend:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Run Frontend
run-frontend:
	cd frontend && npm run dev

# Build Docker Images
docker-build:
	docker build -t log-monitor-backend ./backend
	docker build -t log-monitor-frontend ./frontend

# Start the Application using Docker Compose
docker-up:
	$(DOCKER_COMPOSE) up -d --build

# Stop and Remove Containers
docker-down:
	$(DOCKER_COMPOSE) down

# Run Linting (Python & JavaScript)
lint:
	flake8 backend/
	cd frontend && eslint .

# Run Tests
test:
	pytest backend/tests
	cd frontend && npm test

# Logs
logs:
	$(DOCKER_COMPOSE) logs -f

# Clean up Docker images & volumes
clean:
	$(DOCKER_COMPOSE) down -v
	docker system prune -af
