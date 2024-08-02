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
EOF
USER $USER
ENV SERVICE ${SERVICE}


# Copy all py files and install required dependencies
FROM base as sources
ARG SERVICE
WORKDIR ${HOME}/sources

COPY --chown=$USER:$USER sdk sdk
COPY --chown=$USER:$USER services/${SERVICE}/pyproject.toml services/${SERVICE}/pyproject.toml
RUN <<EOF
find . -name pyproject.toml -exec bash -c \
    'pip --disable-pip-version-check install --user --prefer-binary -e "$(dirname {})"' \;
EOF
COPY --chown=$USER:$USER services/${SERVICE} services/${SERVICE}


# On local dev, just run the python files
FROM base as dev
ARG SERVICE
WORKDIR ${HOME}/sources/services/${SERVICE}

COPY --from=sources ${HOME}/ ${HOME}/
CMD ["bash", "-c", "echo \"${SERVICE}/\" | grep -q / || python -m \"${SERVICE}\" && python -m \"$(echo \"${SERVICE}\" | rev | cut -d/ -f1 | rev)\""]
