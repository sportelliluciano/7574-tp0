#!/bin/sh

# Generates a blob of N bytes, sends it to an echo server and waits
# for its reply. If the reply is the same as the blob sent, the command
# will exit with code 0. Otherwise, it will exit with code 1.
#
# Each run will generate a new random seed to generate the blob. The seed
# can be fixed by setting the environment variable RANDOM to a fixed value.
#
# Usage:
#   ./run-single-test.sh <server> <port> <blob size>
#

log() {
    >&2 echo $1
}

# First `head` gets N random bytes. Base64 adds a little overhead
# for padding. Second `head` ensures that we don't send more than N 
# bytes.
blob=$(head -c "$3" /dev/urandom | base64 -w0 | head -c $3)
result=$(echo $blob | nc $1 $2)

if [[ "$result" == "$blob" ]]; then
    log "[OK ] Test with $3 bytes"
    exit 0
else
    log "[ERR] Test with $3 bytes"
    log "Sent:"
    log "[$blob]"
    log "Got:"
    log "[$result]"
    exit 1
fi
