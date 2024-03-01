import sys
import logging
from search.index import update_indexes


async def exit_bot():
    await update_indexes(rescue=True)
    logging.info('Exiting...')
    sys.exit(0)
