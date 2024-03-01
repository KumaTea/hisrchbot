import os
import logging
from common.data import msg_data_dir
from handlers.register import register_handlers


def starting():
    os.makedirs(msg_data_dir, exist_ok=True)

    register_handlers()

    return logging.info("[Bot] Initialized.")
