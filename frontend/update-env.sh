#!/bin/bash

# Check if .env file exists
if [ -f "/app/.env" ]; then
  # Load environment variables from .env file
  set -o allexport
  source /app/.env
  set +o allexport

  # Update environment files with the loaded values
  echo "export const environment = {" > /app/src/environments/environment.ts
  echo "  production: false," >> /app/src/environments/environment.ts
  echo "  apiKey: '$API_KEY'," >> /app/src/environments/environment.ts
  echo "  host: '$HOST'," >> /app/src/environments/environment.ts
  echo "  clientId: '$CLIENT_ID'" >> /app/src/environments/environment.ts
  echo "};" >> /app/src/environments/environment.ts

  echo "export const environment = {" > /app/src/environments/environment.prod.ts
  echo "  production: true," >> /app/src/environments/environment.prod.ts
  echo "  apiKey: '$API_KEY'," >> /app/src/environments/environment.prod.ts
  echo "  host: '$HOST'," >> /app/src/environments/environment.prod.ts
  echo "  clientId: '$CLIENT_ID'" >> /app/src/environments/environment.prod.ts
  echo "};" >> /app/src/environments/environment.prod.ts
else
  echo "Error: .env file not found. Unable to update environment files."
  exit 1
fi
