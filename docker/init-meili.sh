#!/usr/bin/env bash

docker run \
  -it -d \
  --name meili --restart=unless-stopped -p 7700:7700 \
  -e MEILI_ENV='production' -e MEILI_MASTER_KEY='TelegramHisrchbot' \
  -v /home/kuma/bots/hisrchbot/data/meili:/meili_data \
  getmeili/meilisearch
