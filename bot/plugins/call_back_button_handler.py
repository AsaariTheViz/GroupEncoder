from bot.helper_funcs.utils import on_task_complete, add_task
from bot import (
    AUTH_USERS,
    DOWNLOAD_LOCATION,
    LOG_CHANNEL,
    data,
    pid_list
)
from pyrogram.types import CallbackQuery
import datetime
import logging
import os, signal
import json
import shutil
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
LOGGER = logging.getLogger(__name__)

#from bot.helper_funcs.admin_check import AdminCheck


async def button(bot, update: CallbackQuery):
    cb_data = update.data
    try:
        g = await AdminCheck(bot, update.message.chat.id, update.from_user.id)
        print(g)
    except:
        pass
    LOGGER.info(update.message.reply_to_message.from_user.id)
    if (update.from_user.id == update.message.reply_to_message.from_user.id) or g:
        print(cb_data)
        if cb_data == "fuckingdo":
            if update.from_user.id in AUTH_USERS:
                status = DOWNLOAD_LOCATION + "/status.json"
                with open(status, 'r+') as f:
                    statusMsg = json.load(f)
                    statusMsg['running'] = False
                    f.seek(0)
                    json.dump(statusMsg, f, indent=2)
                    if 'pid' in statusMsg.keys():
                        try:
                            os.kill(statusMsg["pid"], signal.SIGSTOP)
                            os.kill(pid_list[0], signal.SIGSTOP) 
                            del pid_list[0]
                            os.system("rm -rf downloads/*")
                            await bot.delete_messages(update.message.chat.id, statusMsg["message"])
                            #await on_task_complete()
                        except Exception as e:
                            print(e)
                            pass
                        
                        chat_id = LOG_CHANNEL
                        utc_now = datetime.datetime.utcnow()
                        ist_now = utc_now + \
                            datetime.timedelta(minutes=30, hours=5)
                        ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
                        bst_now = utc_now + \
                            datetime.timedelta(minutes=00, hours=6)
                        bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
                        now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
                        await bot.send_message(chat_id, f"**Last Process Cancelled, Bot is Free Now !!** \n\nProcess Done at `{now}`", parse_mode="markdown")
            else:
                try:
                    await update.message.edit_text("You are not allowed to do that 🤭")
                except:
                    pass

        elif cb_data == "fuckoff":
            try:
                await update.message.edit_text("Okay! Fine 🤬")
            except:
                pass
