FROM alpine:3.17

RUN apk --no-cache add netcat-openbsd

WORKDIR /nc-tests
COPY *.sh ./
CMD ["sh", "nc-tests.sh"]