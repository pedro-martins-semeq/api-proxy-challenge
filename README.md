# Proxy API Challenge

This repository contains a dual-component system designed to interact with one of Semeq’s internal staging APIs. It offers:

- **Backend**: A REST API built using **FastAPI**, responsible for authentication and data forwarding.
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

## Setup Instructions

- [Backend Setup — `api/`](./api/README.md)
- [Frontend (TUI) Setup — `tui/`](./tui/README.md)

These documents include environment setup, installation, and usage guidance.

---

## 🛠 Tech Stack

- **FastAPI** — REST API backend
- **Textual** — Terminal User Interface
- **httpx** — HTTP client for upstream communication
- **Python 3.11+**

---

## Notes

- The TUI and API communicate via HTTP; both must be running for full functionality.
- This project was developed as part of an internal challenge at **Semeq**

---

## License

This project is for internal use and not intended for public distribution.

