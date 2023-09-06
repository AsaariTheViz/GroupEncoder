
# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

import os
from bot import data
from bot.plugins.incoming_message_fn import incoming_compress_message_f
from pyrogram.types import Message
from psutil import disk_usage, cpu_percent, virtual_memory, Process as psprocess


def checkKey(dict, key):
  if key in dict.keys():
    return True
  else:
    return False

async def on_task_complete():
    del data[0]
    if len(data) > 0:
      await add_task(data[0])

async def add_task(message: Message):
    try:
        os.system('rm -rf /app/downloads/*')
        await incoming_compress_message_f(message)
    except Exception as e:
        LOGGER.info(e)  
    await on_task_complete()

async def sysinfo(e):
    total, used, free, disk= disk_usage('/')
    total = hbs(total)
    free = hbs(free)
    memory = virtual_memory()
    mem_p = memory.percent
    mem_t = hbs(memory.total)
    mem_a = hbs(memory.available)
    mem_u = hbs(memory.used)
    await e.reply_text(f"**OS:** {platform.system()}\n**Version:** {platform.release()}\n**Arch:** {platform.architecture()}\n**Total Disk Space:** {total}\n**Free:** {free}\n**Memory Total:** {mem_t}\n**Memory Free:** {mem_a}\n**Memory Used:** {mem_u}\n")

