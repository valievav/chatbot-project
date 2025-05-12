#### Django BE + REACT FE + Docker to run env 

- FE http://localhost:5173/
- BE Admin http://localhost:8000/admin/
- BE API http://localhost:8000/api/hello-world/
- To run project `docker compose up --watch --build`

Notes on the project:
1. Project created via `docker run --rm -it -v "${PWD}:/code" -w /code node:22.11 sh -c "npm create vite@5.4 frontend -- --template react && cd frontend && npm install"`
2. To sync docker container changes with local machine (opposite of docker watch, which synchronizes from local to container) `docker compose run --rm -v ${PWD}/frontend:/frontend frontend sh -c "npm install axios"`
3. Add gitignore using common gitignore examples https://github.com/github/gitignore/tree/main
4. To setup Django project run `docker compose run --rm backend sh -c "django-admin startproject backend ."`
5. To create core app for db, run `docker compose run --rm backend sh -c "python manage.py startapp core"`
6. 

