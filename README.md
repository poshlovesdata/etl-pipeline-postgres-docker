CDE assignment for Docker with ETL Pipeline and Postgres DB

1. API data extraction
2. Static typing
3. Git/Github
4. Environment variable
5. Functions (Modularity)
6. Pandas

for netwok

Create a user-defined network:

```bash
docker network create etl-network
```

Start Postgres on that network:

```bash
docker run --name etl-postgres \
  --network etl-network \
  -e POSTGRES_USER=etl_user \
  -e POSTGRES_PASSWORD=etl_pass \
  -e POSTGRES_DB=etl_db \
  -d postgres:15
```

Rebuild & run your ETL container on the same network:

```bash
docker run --network etl-network etl-image
```

Store connection details in environment variables (e.g., .env file).

Mount your .env when running:

```bash
docker run --network etl-network --env-file .env etl-image
```
