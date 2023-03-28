#!/bin/sh

set -e

for blob_size in 8 16 32 64 128 256
do
    sh run-single-test.sh $SERVER_HOST $SERVER_PORT ${blob_size}
done