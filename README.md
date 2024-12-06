# 10x National Address Database Submission Tool (NAD-ST)

## Local Development

To run the app locally, you will need to have Python version 3.11.7 and Node.js
version 18.17.1 installed.

Install [poetry](https://python-poetry.org/docs/#installation) so that you can
run tests and scripts locally.

Clone the repostiory:

```bash
git clone https://github.com/GSA-TTS/10x-nad-st/
```

In order to set up a local development environment, you will need to download
[Docker](https://www.docker.com/).

To set the necessary environment variables, copy the `sample.env` file to a new
file named `.env` in the same directory:

```bash
cp sample.env .env
```

Update all settings defaulted to `<add_a_key_here>`.

Install frontend dependencies and run in development mode:

```bash
cd nad_ch/controllers/web
npm install
npm run dev
```

Return to the project's root directory and run the following command to build
the app and start up its services:

```bash
docker compose up --build
```

To create database migrations (add comment associated with migration in quotes):

```bash
docker exec nad-ch-dev-local poetry run alembic revision --autogenerate -m "ENTER COMMENT"
```

To run database migrations:

```bash
docker exec nad-ch-dev-local poetry run alembic upgrade head
```

To downgrade database migrations:

```bash
docker exec nad-ch-dev-local poetry run alembic downgrade <enter down_revision id>
```

## Testing

Some tests in the test suite are dependent on Minio operations and access key is required. To Create a Minio access key, visit the Minio webui at [minio-webui](localhost:9001) and under User/Access Keys, click Create access key. Save the credentials to your .env file under S3_ACCESS_KEY and S3_SECRET_ACCESS_KEY.

Run the test suite as follows:

```bash
poetry run test
```
