#! /usr/bin/env bash

no_cache="--no-cache"
if test -z "${USE_NO_CACHE}"; then
	no_cache=""
fi

. ./common.sh &&
docker build ${no_cache} --build-arg SWISSKNIFE_VERSION=1.80 --build-arg BARRNAP_VERSION=0.9 --build-arg PROKKA_VERSION=1.14.5 -t ${REGISTRY}/${NAME}:${VERSION} . &&
docker tag ${REGISTRY}/${NAME}:${VERSION} ${REGISTRY}/${NAME}:latest &&
docker system prune -f
