# Running Locally From Scratch

Prerequisites:

- Python 3.11.10
- Node.js 18.17.1
- Docker
- `CLOUDGOV_CLIENT_ID` and `CLOUDGOV_CLIENT_SECRET` keys in `.env` populated
  with valid keys (see `scripts/cloud_gov_setup.sh`) for setup instructions.

1. Start Docker containers

```shell
docker compose up --build
```

2. Run alembic migrations

```shell
docker exec nad-ch-dev-local poetry run alembic upgrade head
```

3. Run seed script

```shell
docker exec nad-ch-dev-local python3 scripts/seed.py
```

4. Install frontend dependencies and build frontend assets

```shell
cd nad_ch/controllers/web
npm install
npm run dev
```

5. Go to `localhost:8080` and opt to log in using cloud.gov.

6. After working through the login process, run a script to activate the newly registered user.

```shell
docker exec nad-ch-dev-local python3 scripts/activate_user.py <email address you used to log in goes here>
```
