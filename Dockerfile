FROM docker:latest as build

ARG PATH_WORKDIR=/opt/aziona-cli
ENV PATH_WORKDIR ${PATH_WORKDIR}

WORKDIR ${PATH_WORKDIR}

ENV build_deps \
		binutils \
        gcc \
        musl-dev
        
ENV persistent_deps \
        curl \
        bash \
        gettext \
        python3 \
        py3-pip \
        jq \
        git \
        make \
        acl

# Install build and persistent dependencies
RUN apk upgrade --update-cache --available \
    && apk update \ 
    && apk add --no-cache --virtual .build-dependencies $build_deps \
    && apk add --no-cache --virtual .persistent-dependencies $persistent_deps \
    && python3 -m pip install --upgrade pip

ARG PIP_DEFAULT_TIMEOUT=100
ENV PIP_DEFAULT_TIMEOUT ${PIP_DEFAULT_TIMEOUT}

ARG AZIONA_CLI_NAME="aziona"
ENV AZIONA_CLI_NAME ${AZIONA_CLI_NAME}

ARG AZIONA_CLI_VERSION
ENV AZIONA_CLI_VERSION ${AZIONA_CLI_VERSION}

ARG AZIONA_CLI_BUILDFILE
ENV AZIONA_CLI_BUILDFILE ${AZIONA_CLI_BUILDFILE}

COPY . ${PATH_WORKDIR}/app

# Install aziona-cli from local file
RUN if [[ "${AZIONA_CLI_BUILDFILE}" == "true" ]]; then \
    echo "AZIONA CLI: build local file" && \
    cd ${PATH_WORKDIR}/app && \
    chmod +x -R scripts && \
    make build-wheel && \
    pip install dist/$(ls -t -1 dist | head -n 1) && \
    aziona-dependencies \
; fi

# Install aziona-cli from pypi.org
RUN if [[ "${AZIONA_CLI_BUILDFILE}" != "true" ]]; then \
    if [[ -z "${AZIONA_CLI_VERSION}" ]] ; then \
        echo "AZIONA CLI: latest version" && \
        pip3 install ${AZIONA_CLI_NAME} \
    ; else \
        echo "AZIONA CLI: ${AZIONA_CLI_VERSION} version" && \
        pip3 install ${AZIONA_CLI_NAME}==${AZIONA_CLI_VERSION} \
    ; fi && \
    aziona-dependencies \
; fi

# Remove build depends
RUN apk del -f .build-dependencies && \
    rm -Rf /var/cache/apk/* && \
    rm -Rf ${PATH_WORKDIR}/app

ENTRYPOINT [ "aziona" ]