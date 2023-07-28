# Setup
```
export dockerhub_username='{dockerhub_username}'
export dockerhub_password='{dockerhub_password}'
```

# Run
## Fresh build
```
docker-compose down -v && \
    docker system prune -af && \
    docker-compose up --build
```

## Cycle build
```
docker-compose down -v && \
    docker-compose up --build
```