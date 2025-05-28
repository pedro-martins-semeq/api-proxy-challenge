# Proxy API Challenge

This repository contains a dual-component system designed to interact with one of Semeq’s internal staging APIs. It offers:

- **Backend**: An HTTP API built using **FastAPI**, responsible for authentication and data forwarding.
- **Frontend**: A terminal user interface (TUI) built using **Textual**, providing a user-friendly CLI for interacting with the backend.

---

## Project Structure

```
api-proxy-challenge/
├── api/      # FastAPI backend
├── tui/      # Terminal-based UI client
└── README.md # This file
```

---

## Getting Started

Clone the repository:

```bash
git clone https://github.com/pedro-martins-semeq/api-proxy-challenge
cd api-proxy-challenge
```

Each module has its own setup instructions inside its respective folder.

---


## 🛠 Tech Stack

- **FastAPI** — REST API backend
- **Textual** — Terminal User Interface
- **httpx** — HTTP client for upstream communication
- **Python 3.11+**

---

## Requirements
**If you opt to run the application with docker:**
- `Docker` (tested with v28.0+)
  - Be sure to have **host networking** enable in your Docker Engine

**Otherwise:**
- `Python 3.11+`
- `Git`

## Docker Setup and Usage

This project includes Docker configurations to simplify running the API and TUI services, either separately or together.

### Available Docker Compose files:

- `docker-compose.yaml` — Runs both `api` and `tui` services together.
- `api/docker-compose.api.yaml` — Runs only the API service.
- `tui/docker-compose.tui.yaml` — Runs only the TUI service.

### Running both services (API + TUI):

```bash
docker compose up --build
```

This command uses the root `docker-compose.yaml` to build and start both containers.

### Running API service only:

```bash
docker compose -f ./api/docker-compose.api.yaml up --build
```

Start only the backend API container.

### Running TUI service only:

```bash
docker compose -f ./tui/docker-compose.tui.yaml up --build
```

Start only the terminal UI container. Make sure the API service is accessible externally (e.g., running on the host machine or in another container).

### Convenience scripts

You can also use provided shell scripts for convenience:

- `./docker_api_launch.sh` — Launches only the API container.
- `./docker_tui_serve.sh` — Launches only the TUI container.

Make sure these scripts are executable:

```bash
chmod +x docker_api_launch.sh docker_tui_serve.sh
```

And run them as:

```bash
./docker_api_launch.sh
./docker_tui_serve.sh
```

---

## Individual Setup Instructions

- [Backend Setup — `api/`](./api/README.md)
- [Frontend (TUI) Setup — `tui/`](./tui/README.md)

These documents include environment setup, installation, and usage guidance for each component.

---

## Notes

- The TUI and API communicate via HTTP; both must be running for full functionality.
- This project was developed as part of an internal challenge at **Semeq**.

---

## License

This project is for internal use and not intended for public distribution.
