CDE assignment for Docker with ETL Pipeline and Postgres DB

1. API data extraction
2. Static typing
3. Git/Github
4. Environment variable
5. Functions (Modularity)
6. Pandas

for netwok
1. Create a network:

```bash
docker network create etl-postgres-network
```

2. Build etl image
```bash
docker build -t etl-job .
```

3. Start Postgres using the .env file
```bash
docker run --name postgres-db \
  --network etl-postgres-network \
  --env-file .env \
  -d postgres:15
```

4. Run the ETL container using the same .env file
```bash
docker run --rm \
  --name etl-job-container \
  --network etl-postgres-network \
  --env-file .env \
  etl-job
```