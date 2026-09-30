FROM mcr.microsoft.com/devcontainers/python:3.14-trixie AS toolchain

WORKDIR /tmp
## hadolint
ARG HADOLINT_URL="https://github.com/hadolint/hadolint/releases/download/v2.12.0/hadolint-Linux-x86_64"
RUN curl -fsSL ${HADOLINT_URL} -o hadolint  &&\
    install -m 755 hadolint /usr/local/bin/hadolint
## python
# uv
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ARG UV_URL="https://astral.sh/uv/install.sh"
RUN curl -LsSf ${UV_URL} | sh && \
    install -m755 /root/.local/bin/uv /usr/local/bin/uv

## git
WORKDIR /usr/share/doc/git/contrib/diff-highlight
RUN make && \
    install -m 755 diff-highlight /usr/local/bin/diff-highlight

# ======================================================================

FROM mcr.microsoft.com/devcontainers/python:3.14-trixie

RUN DEBIAN_FRONTEND=noninteractive\
    apt-get -qq update &&\
    apt-get -qq install --no-install-recommends -y \
    # utility
    peco\
    ripgrep\
    vim\
    # for container
    supervisor\
    # for vision
    libegl1 \
    libgles2 \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean\
    && rm -rf /var/lib/apt/lists/*

COPY --from=toolchain /usr/local/bin /usr/local/bin
COPY --from=toolchain /etc/bash_completion.d /etc/bash_completion.d

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -q -r /tmp/requirements.txt

COPY ./supervisor/ /etc/supervisor
