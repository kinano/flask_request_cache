# flask_request_cache
Leverage flask request context (g object) to cache expensive functions during the lifetime of one request

# How do I run this on my local machine?

```
# Run the application
docker-compose up

# Observe the logs in a separate terminal
docker ps -a # Get CONTAINER_ID
docker exec -ti CONTAINER_ID tail -f /tmp/flask_log.log

```