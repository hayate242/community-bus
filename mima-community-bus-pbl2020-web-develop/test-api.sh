#!/bin/sh
DEFAULT_TEST_MODE='develop'
DEVELOP_URL='http://localhost:8000'
PRODUCTION_URL='https://b-map.pbl.jp'

read -p "Please select test mode [develop or staging or production](Default: ${DEFAULT_TEST_MODE}): " TEST_MODE
TEST_MODE=${TEST_MODE:-${DEFAULT_TEST_MODE}}

if [ ${TEST_MODE} = 'develop' ]; then
  BASE_URL=${DEVELOP_URL}
elif [ ${TEST_MODE} = 'production' ]; then
  BASE_URL=${PRODUCTION_URL}
else
  echo "${TEST_MODE} is not a test mode"
  exit
fi

echo "Start api test for ${BASE_URL}"

docker run --rm\
  -v $(pwd)/mimap-test.postman_collection.json:/etc/newman/mimap-test.postman_collection.json \
  -t postman/newman:alpine \
  run mimap-test.postman_collection.json \
  --env-var BASE_URL=${BASE_URL}