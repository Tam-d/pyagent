FROM ubuntu:24.04

WORKDIR /app

ARG GO_VERSION="go1.25.4"
ARG GO_URL="https://go.dev/dl/${GO_VERSION}.linux-amd64.tar.gz"

ARG BOOT_DEV_CLI_URL="github.com/bootdotdev/bootdev@latest"

#install git
RUN apt update && apt install -y \
software-properties-common && \
add-apt-repository -y ppa:git-core/ppa && \
apt install -y git

RUN apt install -y curl

#install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

#install go
RUN curl -OL ${GO_URL} && \
    rm -rf /usr/local/go && \
    tar -C /usr/local -xzf ${GO_VERSION}.linux-amd64.tar.gz

ENV PATH=$PATH:/usr/local/go/bin

#install bootdev cli
RUN go install ${BOOT_DEV_CLI_URL}

ENV PATH=$PATH:/root/go/bin