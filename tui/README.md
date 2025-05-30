# Proxy API - Terminal User Interface (TUI)

This is the frontend client service of the application, built using **Textual**. 

>#### The recommended way to build the project is to run `docker compose up --build` on the root folder

### The TUI Features:
- **A simple to use terminal interface to connect with the backend:**

<img src="./assets/readme_images/connection_screen.png" width=500>

- **Authentication modal screen:**

<img src="./assets/readme_images/login_screen.png" width=500>

- **A main screen with:**
  - Header filled with **usercorp** user information.
  - Scrollable box with user **associated corporations**.
  - Scrollable body with all user **associated sites**.

<img src="./assets/readme_images/main_screen.png" width=500>

- **Access and refresh token session storage with access token refresh when expired.**

<img src="./assets/readme_images/token_refresh.png" width=500>

- **An accordion modal screen to visualize an user associated site tree:**

<img src="./assets/readme_images/implantation_tree_modal.png" width=500>

- **Different color schemes:**

<img src="./assets/readme_images/color_schemes.png" width=500>

<img src="./assets/readme_images/theme_gruvbox_sample.png" width=300>
<img src="./assets/readme_images/theme_monokai_sample.png" width=300>

---

# Running the TUI.

## If you want to run just the TUI frontend separately

### Option 1. Serve the TUI using the TUI-Only docker-compose
To serve (web host) only the TUI service, use its specific `docker-compose.tui.yaml`:

```bash
cd ./tui
docker compose -f ./docker-compose.tui.yaml up --build
```

---

### Option 2. Serve the TUI directly with Docker
You can build and run the TUI container manually without `docker-compose`:

```bash
# On the ./tui directory:
cd ./tui

# Build the TUI Docker image
docker buildx build -t proxy-tui .

# Run the container
docker run --name proxy-tui --network host proxy-tui
```

---

### Option 3. Run the TUI locally without docker
Clone the repository
```bash
git clone https://github.com/pedro-martins-semeq/api-proxy-challenge
cd api-proxy-challenge/tui
```

**After clonning the repo, you must create and activate the virtual environment:**

>You can use the `setup.sh` file to create a venv in a `.venv/` folder, activate it and install the dependencies listed in the `requirements.txt` file:
>```bash
>source setup.sh
>``` 
>
> ### **or**
>
>You can setup the environment manually with the following commands:
>```bash
>python3 -m venv .venv
>source ./.venv/bin/activate
>pip install -r requirements.txt
>```
> ---

#### Start the TUI Application
You may start the application directly in your terminal window:
```bash
textual run main.py
```

#### OR

You can serve the application to access the interface in a web browser
```bash
textual serve --host 127.0.0.1 -p 3000 main.py
```

> With this command, the TUI will be available at:
> <br>http://127.0.0.1:3000 <br>
> Be sure that the port 3000 is available when serving the app or configure a port (`-p` parameter) of your choice.

### TUI Running on web browser:

<img src="./assets/readme_images/web_browser_serve.png" width=750>

---

## Notes
- This service uses `httpx` for HTTP requests to external APIs.
- For more request formatting info: the `./src/api-client/api_client.py` module provides all the HTTP client app logic.