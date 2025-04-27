# copy init files for database
FROM postgres:latest

ARG INITDIR="/docker-entrypoint-initdb.d/"
ARG STORESCHEMA="./01-store-schema.sql"
ARG BANKSCHEMA="./00-bank-schema.sql"

COPY ${BASNKSHEMA} ${INITDIR}
COPY ${STORESCHEMA} ${INITDIR}

# initialize the database during the build
RUN echo "exit 0" > ${INITDIR}99-exit_before_boot.sh

