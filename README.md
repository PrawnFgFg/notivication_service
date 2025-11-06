

docker network create myNetwork


docker run --name notification_service_docker_cont \
    -p 6432:5432 \
    -e POSTGRES_USER=mvzfgfg \
    -e POSTGRES_PASSWORD=stick7856doc \
    -e POSTGRES_DB=notification_service \
    --network=myNetwork \
    --volume pg-notification-data:/var/lib/postgresql/data \
    -d postgres:16


docker run --name notification_cache \
    -p 7379:6379 \
    --network=myNetwork \
    -d redis:7.4


docker run --name notification_back \
    -p 7777:8000 \
    --network=myNetwork \
    notification_image


docker build -t "notification_image" .