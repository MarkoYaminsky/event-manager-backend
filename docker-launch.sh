BUILD_OPTION=""

if [ "$1" == "build" ]; then
  BUILD_OPTION="--build"
fi

docker-compose down
docker-compose up $BUILD_OPTION
