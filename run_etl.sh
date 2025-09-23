#!/bin/bash
# fail safe
set -e

# declare empty array to store .env values
env_variables=()

# create an array to store .env keys
variable_name=("POSTGRES_USER" "POSTGRES_PASSWORD" "POSTGRES_DB")

output_file=".env"

seperator="#########################"
# check if .env file already exists
if [ -f "$output_file" ]; then
    echo ".env file already exists. skipping environment variable setup."

else
    echo "Starting scripts..."

    # create .env, if exists clear content
    # > "$output_file"

    # loop through .env keys to collect values from user
    for item in "${variable_name[@]}"; do
        read -p "Enter env variable for $item: " input
        # echo "$item"
        env_variables+=($input)
    done

    # assign .env keys to values
    for index in "${!variable_name[@]}"; do
        echo "${variable_name[$index]}=${env_variables[$index]}" >> "$output_file"
    done

    # accept db_host from user as container name
    read -p "Last one i promise, Enter a name for your postgres container (e.g postgres-db): " pg_container
    echo "DB_HOST=$pg_container" >> "$output_file"

    # save demo coingecko api key to .env
    echo "COIN_GECKO_API_KEY=CG-Bw43gCy7qQjhc3M77x54L2tT" >> "$output_file"

    echo "environment variables saved to .env file."
fi
# export .env 
set -a
source .env
set +a


# create network
docker network create etl-postgres-network 2>/dev/null || true

# build etl image from etl.py
docker build -t etl-job .

# remove old postgres container if it exists
if [ "$(docker ps -aq -f name=^${DB_HOST}$)" ]; then
  echo "Removing old container: $DB_HOST"
  docker rm -f "$DB_HOST"
fi

# start postgres using the .env file
docker run --name "$DB_HOST" \
  --network etl-postgres-network \
  --env-file .env \
  -d postgres:15

# wait for postgres to be ready 
until docker exec "$DB_HOST" pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
    echo "Waiting for postgres ($DB_HOST) to be ready..."
    sleep 2
done
echo "postgres is ready.."

echo "running etl script..."

# run the ETL container using the same .env file
docker run --rm \
  --name etl-job-container \
  --network etl-postgres-network \
  --env-file .env \
  etl-job

echo "script completed."

echo "$seperator"
echo "run sql queries in your postgres container. \q to leave container"

# docker run --name "$DB_HOST" \
#   --network etl-postgres-network \
#   --env-file .env \
#   -d postgres:15 && \
# docker exec -it "$DB_HOST" psql -U "$POSTGRES_USER"
echo "$seperator"

echo "run 'select * from coin_price' to get started"
docker exec -it "$DB_HOST" psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"