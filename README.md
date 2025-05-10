
Notes on the project:
1. Project created via `docker run --rm -it -v "${PWD}:/code" -w /code node:22.11 sh -c "npm create vite@5.4 frontend -- --template react && cd frontend && npm install"` 
2. To run project `docker compose up --watch --build`
3. App available at http://localhost:5173/
4. Make sure docker container changes are being synced to local machine (opposite of docker watch, which synchronizes from local to container) `docker compose run --rm -v ${PWD}/frontend:/frontend frontend sh -c "npm install axios"`