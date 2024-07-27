ARG DOCKERHUB_MIROR="docker.io"
FROM ${DOCKERHUB_MIROR}/library/python:3.12.4-slim-bookworm

ENV USER=1000
ENV HOME=/home/$USER
ENV PATH=$PATH:$HOME/.local/bin

WORKDIR $HOME/app

USER $USER

COPY --chown=$USER:$USER requirements.txt requirements.txt

RUN pip install --user -r requirements.txt --prefer-binary --no-deps

COPY --chown=$USER:$USER maximus maximus

CMD ["python", "-m", "maximus"]
