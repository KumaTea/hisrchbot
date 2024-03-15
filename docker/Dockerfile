FROM kumatea/pyrogram:latest

ENV PIP_PKGS="aiohttp apscheduler beautifulsoup4 meilisearch pyrogram tgcrypto uvloop"

# Create conda environment
RUN set -ex && \
    pip install $PIP_PKGS --prefer-binary && \
    rm -rf /root/.cache/*


# Set entrypoint
ENTRYPOINT ["/bin/bash", "/home/kuma/bots/hisrchbot/docker/run-docker.sh"]
