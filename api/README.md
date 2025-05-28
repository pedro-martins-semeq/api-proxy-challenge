# Proxy API - Backend

This is the backend service of the application, built using **FastAPI**. It provides endpoints for authentication, token validation, site queries and static info for one of Semeq's internal staging apis.

>#### The recommended way to build the project is to run `docker compose up --build` on the root folder

---

## If you want to run only the API backend separately:

### Option 1. Run the API using the API-Only docker-compose
To run only the API service, use its specific `docker-compose.api.yaml`:

```bash
cd ./api
docker compose -f ./docker-compose.api.yaml up --build
```

---

### Option 2. Run the API directly with Docker
You can build and run the backend container manually without `docker-compose`:

```bash
cd ./api

# Build the API Docker image
docker buildx build -t proxy-api .

# Run the container
docker run -p 8000:8000 proxy-api
```

---

### Option 3. Run the API locally without docker
Clone the repository
```bash
git clone https://github.com/pedro-martins-semeq/api-proxy-challenge
cd api-proxy-challenge/api
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

#### Start the API Server
```bash
uvicorn app.main:app --reload
```

> By default, the API will be available at:
> <br>http://127.0.0.1:8000 <br>
> Be sure that the port 8000 is available when launching the server.

---

## Main Endpoints
- #### `POST /auth/login` <br>
    Communicates with the authentication service of the upstream API 

    > ### Request Body
    >```json
    > {
    >    "username": "string",
    >    "password": "string"
    > }
    >```
    > ---

    > ### Status Code 200 - Response Body
    >```json
    >  {
    >     "refresh": "jwt_token_string",
    >     "access": "jwt_token_string"
    >  }
    >```
    > ---

- #### `POST /auth/token/verify`
    Returns a status code 200 if the upstream API validates the request body's token
    > ### Request Body
    >```json
    > {
    >    "token": "jwt_token_string",
    > }
    >```
    > ---

    > ### Status Code 200 - Response Body
    >```json
    >  {}
    >```
    > ---

- #### `POST /auth/token/refresh`
    Returns a status code 200 if the upstream API vallidates the request body's token
    > ### Request Body
    >```json
    > {
    >    "token": "jwt_token_string",
    > }
    >```
    > ---

    > ### Status Code 200 - Response Body
    >```json
    >  {}
    >```
    > ---

- #### `GET /usercorp` (Bearer Token authentication required) 
    Retrieve the access token authenticated user information

    > ### Status Code 200 - Response Body
    >```json
    >{
    >	"user": {
    >		"id": int,
    >		"username": "string",
    >		"first_name": "string",
    >		"last_name": "string",
    >		"email": "string"
    >	},
    >	"corporation": [
    >		{
    >			"id": int,
    >			"name": "string"
    >		},
    >           ...
    >		{
    >			"id": int,
    >			"name": "string"
    >		},
    >	],
    >	"sites": [
    >		{
	>           "id": int,
    >			"name": "string",
    >			"corporation": int
    >		},
    >           ...
    >		{
    >			"id": int,
    >			"name": "string",
    >			"corporation": int
    >		}
    >	],
    >	"notification": []
    >}
    >```
    > ---

- #### `GET /implantation/mobile/tree?site={id}` (Bearer Token authentication required)
    Retrieve the implantation site tree from the site with the given id
    
    > ### Status Code 200 - Response Body (Example)
    >   ```json
    >{
    >"id": 12345,
    >"name": "Enterprise",
    >"revision": 1,
    >"tree": [
    >    {
    >        "id": 54321,
    >        "refresh_setups": false,
    >        "asset_type": 271,
    >        "original_asset_type": 271,
    >        "group": "compressor",
    >        "criticality": null,
    >        "functional_location": null,
    >        "size": null,
    >        "status": true,
    >        "name": "AIR COMPRESSOR 02",
    >        "tag": "C123003",
    >        "level": 3,
    >        "order": 5,
    >        "parent": 123455,
    >        "site": 123454
    >    },
    >       ...
    >    {
    >        "id": 54322,
    >        "refresh_setups": false,
    >        "asset_type": 272,
    >        "original_asset_type": 272,
    >        "group": "gearbox",
    >        "criticality": null,
    >        "functional_location": null,
    >        "size": null,
    >        "status": true,
    >        "name": "REDUCTOR RED-3 CHAIN",
    >        "tag": "R501028",
    >        "level": 3,
    >        "order": 7,
    >        "parent": 123456,
    >        "site": 123453
    >    }
    >]}
    >```
    > ---

---

## Other Endpoints (Not supported by the  client TUI)
- #### `GET /mobile/info?site={id}` (Bearer Token authentication required)
- #### `GET /implantation/mobile/static`
- #### `GET /implantation/mobile/static/get_lubricants`

---

## Notes
- This service uses `httpx` for HTTP requests to external APIs.
- The routes depend on upstream services configured in environment variables
- For more request formatting info: the `core/http_proxy.py` module provides the generic HTTP fowarding layer