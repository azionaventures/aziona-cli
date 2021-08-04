FROM docker:latest as build

ARG PATH_WORKDIR=/opt/aziona-cli
ENV PATH_WORKDIR ${PATH_WORKDIR}

WORKDIR ${PATH_WORKDIR}

ENV build_deps \
		binutils
        
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

# Remove build depends
RUN apk del -f .build-dependencies \
    && rm -rf /var/cache/apk/*

ARG AZIONA_CLI_NAME="aziona"
ENV AZIONA_CLI_NAME ${AZIONA_CLI_NAME}

ARG AZIONA_CLI_VERSION
ENV AZIONA_CLI_VERSION ${AZIONA_CLI_VERSION}

# Install aziona-cli
RUN if [[ -z "${AZIONA_CLI_VERSION}" ]] ; then \
    echo "AZIONA CLI: latest version" && \
    pip3 install ${AZIONA_CLI_NAME} \
; else \
    echo "AZIONA CLI: ${AZIONA_CLI_VERSION} version" && \
    pip3 install ${AZIONA_CLI_NAME}==${AZIONA_CLI_VERSION} \
; fi && \
    aziona-dependencies

# Download deafualt template. 
# TODO remove when aziona-cli donwload terraform module in runtime
ARG PATH_TERRAFORM=${PATH_WORKDIR}/terraform
ENV PATH_TERRAFORM ${PATH_TERRAFORM}
RUN git clone https://github.com/azionaventures/aziona-cli-terraform /tmp/terraform && \
    mkdir ${PATH_TERRAFORM} && \
    mv /tmp/terraform/modules/* ${PATH_TERRAFORM} && \
    rm -Rf /tmp/terraform ${PATH_TERRAFORM}/.gitignore

ENTRYPOINT [ "aziona" ]