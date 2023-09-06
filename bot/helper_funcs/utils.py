
# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

import os, asyncio, pyrogram, psutil, platform, time
from bot import data
from bot.plugins.incoming_message_fn import incoming_compress_message_f
from pyrogram.types import Message
from psutil import disk_usage, cpu_percent, virtual_memory, Process as psprocess


def checkKey(dict, key):
  if key in dict.keys():
    return True
  else:
    return False

def hbs(size):
    if not size:
        return ""
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "B", 1: "K", 2: "M", 3: "G", 4: "T", 5: "P"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"

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
    message = await e.reply_text(
        "🚀 <b>Getting System Information...</b>",
        quote=True)
    start_time = time.monotonic()
    last_content = None

    os_info = f"<b>Operating System:</b> {platform.system()} {platform.release()} ({platform.machine()})\n\n"
    os_info += "".join(["━"] * 21) + "\n"

    while time.monotonic() - start_time <= 137:
        cpu_usage = psutil.cpu_percent(percpu=True)
        cpu_freq = psutil.cpu_freq()
        cpu_count = psutil.cpu_count(logical=False)
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_count_virtual = cpu_count_logical - cpu_count
        ram_stats = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        dl_size = psutil.net_io_counters().bytes_recv
        ul_size = psutil.net_io_counters().bytes_sent

        cpu_bar = ['⬢' * int(percent / 10) + '⬡' * (10 - int(percent / 10)) for percent in cpu_usage]
        freq_current = f"{round(cpu_freq.current / 1000, 2)} GHz"
        if cpu_freq.min > 0 and cpu_freq.max > 0:
            freq_min = f"{round(cpu_freq.min / 1000, 2)} GHz"
            freq_max = f"{round(cpu_freq.max / 1000, 2)} GHz"
            freq_info = f"<b>CPU Frequency:</b> {freq_current} (<b>Min:</b> {freq_min}, <b>Max:</b> {freq_max})\n\n"
        else:
            freq_info = f"🖥️ <b>CPU Frequency:</b> {freq_current}\n\n"

        ram_perc = int(ram_stats.percent)
        ram_used = psutil._common.bytes2human(ram_stats.used)
        ram_total = psutil._common.bytes2human(ram_stats.total)
        ram_bar = '▪️' * int(ram_perc / 10) + '▫️' * (10 - int(ram_perc / 10))
        if ram_perc > 80:
            ram_emoji = "‼️"
        elif ram_perc > 20:
            ram_emoji = "🚀"
        else:
            ram_emoji = "🎮"
        ram_info = f"{ram_emoji} <b>RAM Usage:</b> {ram_perc}%\n[{ram_bar}]\n<b>Used:</b> {ram_used} <b>of</b> {ram_total}\n<b>Free :</b>  {psutil._common.bytes2human(ram_stats.available)}\n"

        disk_perc = int(disk.percent)
        disk_used = psutil._common.bytes2human(disk.used)
        disk_total = psutil._common.bytes2human(disk.total)
        disk_bar = '▪️' * int(disk_perc / 10) + '▫️' * (10 - int(disk_perc / 10))
        disk_info = f"💾 <b>Disk Usage:</b> {disk_perc}%\n[{disk_bar}]\n<b>Used:</b> {disk_used} <b>of</b> {disk_total}\n<b>Free :</b>  {psutil._common.bytes2human(disk.free)}\n"

        sys_info = f"{os_info}{freq_info}"
        for i, percent in enumerate(cpu_usage[:cpu_count]):
            if cpu_count > 9 and i < 9:
                core_num = f"0{i+1}"
            else:
                core_num = str(i+1)
            sys_info += f"[{cpu_bar[i]}] <b>Core {core_num}:</b> {percent:.1f}%\n"
        sys_info += f"\n\t◉ <b>Physical Cores:</b> {cpu_count}\n"
        if cpu_count_virtual > 0:
            sys_info += f"\t◉ <b>Logical Cores:</b> {cpu_count_virtual}\n"
        else:
            sys_info += ""
        sys_info += "".join(["━"] * 21) + "\n"
        sys_info += ram_info
        sys_info += "".join(["━"] * 21) + "\n"
        sys_info += disk_info
        sys_info += "".join(["━"] * 21) + "\n"
        sys_info += f"🔻 <b>DL :</b> {psutil._common.bytes2human(dl_size)} <b>|</b> 🔺 <b>UL :</b> {psutil._common.bytes2human(ul_size)}"

        if sys_info != last_content:
            await message.edit_text(sys_info)
            last_content = sys_info

        await asyncio.sleep(3)

    await message.edit_text("🎯 <b>Time Limit Reached!</b>")
