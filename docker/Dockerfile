FROM kumatea/bot:latest

ENV CONDA_PKGS="apscheduler pyrogram uvloop"
ENV PIP_PKGS="meilisearch tgcrypto"

# Create conda environment
RUN set -ex && \
    eval "$(/opt/conda/bin/conda shell.bash hook)" && \
    conda create -n hs $CONDA_PKGS -y && \
    conda clean -afy && \
    conda activate hs && \
    pip install $PIP_PKGS --prefer-binary --extra-index-url https://ext.kmtea.eu/cdn && \
    rm -rf /root/.cache/*


# Set entrypoint
ENTRYPOINT ["/bin/bash", "/home/kuma/bots/hisrchbot/docker/run-docker.sh"]
