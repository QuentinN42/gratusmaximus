ARG DOCKERHUB_MIROR="docker.io"
# https://hub.docker.com/_/python/tags?page=&page_size=&ordering=&name=3.11.
FROM ${DOCKERHUB_MIROR}/library/python:3.11.9-slim-bookworm

ARG SERVICE

ENV USER=1000
ENV HOME=/home/$USER
ENV PATH=$PATH:$HOME/.local/bin

WORKDIR $HOME/app
RUN <<EOF
useradd --create-home --home-dir $HOME --uid $USER --shell /bin/bash $USER
mkdir -p $HOME/.local/bin $HOME/.local/lib/python3.11/site-packages
chown -R $USER:$USER $HOME
EOF
USER $USER

COPY --chown=$USER:$USER sdk sdk
COPY --chown=$USER:$USER services/${SERVICE}/pyproject.toml services/${SERVICE}/pyproject.toml

RUN <<EOF
find . -name pyproject.toml -exec bash -c \
    'pip --disable-pip-version-check install --user --prefer-binary -e "$(dirname {})"' \;
EOF

COPY --chown=$USER:$USER . .

COPY --chown=$USER:$USER services/${SERVICE} services/${SERVICE}

WORKDIR /opt

CMD ["python", "-m", "maximus"]
