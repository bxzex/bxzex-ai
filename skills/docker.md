---
name: docker
description: Writing a Dockerfile, building and running containers, using docker compose, reading logs and cleaning up.
---
# Docker

Check it works first: `docker version` and `docker ps`. If the daemon is not running, start Docker Desktop on macOS or Windows, or `sudo systemctl start docker` on Linux. On WSL, Docker Desktop must have WSL integration on.

**Dockerfile (Node example)**
```
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```
Copy the dependency files and install before copying the rest, so the install layer is cached. Pin a version tag, not `latest`. Python is the same idea with `python:3.12-slim`, `requirements.txt` and `pip install --no-cache-dir -r`.

Add a `.dockerignore`: `node_modules`, `.git`, `.env`, `dist`, `*.log`. Never bake secrets into an image.

**Build and run**
```
docker build -t myapp .
docker run --rm -p 8080:3000 myapp
```
`-p HOST:CONTAINER` publishes a port. The app inside must listen on `0.0.0.0`, not `127.0.0.1`, or the port will not answer. Test with `curl -sI localhost:8080`.
- Background: `docker run -d --name myapp -p 8080:3000 myapp`
- Env vars: `-e KEY=value` or `--env-file .env`
- Volume for data: `-v mydata:/var/lib/data`. Mount code for dev: `-v "$PWD":/app`.

**Compose** (`compose.yaml`)
```
services:
  web:
    build: .
    ports: ["8080:3000"]
    env_file: .env
    depends_on: [db]
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes: ["pgdata:/var/lib/postgresql/data"]
volumes:
  pgdata:
```
Run `docker compose up -d --build`, stop with `docker compose down` (add `-v` only if you want the data gone).

**Logs and debugging**
- `docker ps -a` shows status; "Exited (1)" means it crashed.
- `docker logs --tail 100 -f myapp` or `docker compose logs -f web`.
- Shell inside: `docker exec -it myapp sh`.

**Clean up**
- `docker image prune` removes dangling images.
- `docker system df` shows disk use.
- `docker system prune` removes stopped containers and unused networks; ask the user before adding `-a` or `--volumes`.

Pitfalls: port already in use (`lsof -i :8080`), wrong build context, forgetting `--rm` and piling up containers.
