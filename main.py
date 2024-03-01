from common.data import debug_mode

if not debug_mode:
    import uvloop
    uvloop.install()

from bot.session import bot, logging
from bot.starting import starting


starting()


if __name__ == '__main__':
    try:
        bot.run()
    except Exception as e:
        logging.exception(str(e))
        import asyncio
        from bot.exiting import exit_bot
        asyncio.run(exit_bot())
