ARG DOCKERHUB_MIROR="docker.io"
# https://hub.docker.com/_/python/tags?page=&page_size=&ordering=&name=3.11.
FROM ${DOCKERHUB_MIROR}/library/python:3.11.9-slim-bookworm as base
ARG SERVICE

ENV USER=1000
ENV HOME=/home/$USER
ENV PATH=$PATH:${HOME}/.local/bin
RUN <<EOF
useradd --create-home --home-dir ${HOME} --uid $USER --shell /bin/bash $USER
mkdir -p ${HOME}/.local/bin ${HOME}/.local/lib/python3.11/site-packages
chown -R $USER:$USER ${HOME}
pip install uv
EOF
USER $USER
ENV SERVICE ${SERVICE}


# Copy all py files and install required dependencies
FROM base as sources
ARG SERVICE
WORKDIR ${HOME}/sources

COPY --chown=$USER:$USER pyproject.toml uv.lock ./
RUN uv sync
COPY --chown=$USER:$USER services/ services/
COPY --chown=$USER:$USER sdk/ sdk/
CMD ["bash", "-c", "uv run python -m services.${SERVICE}"]
