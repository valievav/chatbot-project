#### Django BE + REACT FE + Docker to run env 

- FE Vite + React http://localhost:5173/
- BE Django Admin http://localhost:8000/admin/
- BE Django REST API http://localhost:8000/api/hello-world/
- To run project `docker compose up --watch --build`

Notes on the project:
1. Project created via `docker run --rm -it -v "${PWD}:/code" -w /code node:22.11 sh -c "npm create vite@5.4 frontend -- --template react && cd frontend && npm install"`
2. To sync docker container changes with local machine (opposite of docker watch, which synchronizes from local to container) `docker compose run --rm -v ${PWD}/frontend:/frontend frontend sh -c "npm install axios"`
3. Add gitignore using common gitignore examples https://github.com/github/gitignore/tree/main
4. To setup Django project run `docker compose run --rm backend sh -c "django-admin startproject backend ."`
5. To create core app for db, run `docker compose run --rm backend sh -c "python manage.py startapp core"`
6. To create migrations for new models, run `docker compose run --rm backend sh -c "python manage.py makemigrations"`
7. To create superuser for db, run `docker compose run --rm backend sh -c "python manage.py createsuperuser"`
   (root, admin@admin.com, admin)
8. To run queries in PGAdmin -> add server (host 127.0.0.1, port 5433, username user, password localpass)
9. To test task run, open interactive shell `docker compose run --rm backend sh -c "python manage.py shell"`
and run `from core import tasks; tasks.hello_task('Alice')` to run task directly as a function synchronously w/o celery 
OR `tasks.hello_task.delay('Lily')` / `tasks.hello_task.apply_async(args=["Lily2"], countdown=10)` to run asynchronously with celery.
10.  
