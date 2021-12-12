import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)
spam_chats = []

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply(
    "**Salam mən @A_l_i_y_e_v_d_i tərəfindən yaradılan tag botuyam  məni guruplara ekləyərək bütün üzvləri tag edə bilərəm🤓\n/yardım ** yazaraq daha ətraflı məlumat ala bilərsiniz",
    link_preview=False,
    buttons=(
      [
        Button.url('💭 Gurup', 'https://t.me/iron_Blood_Gurup'),
        Button.url('🌐 Support', 'https://t.me/NEXUS_MMC')
      ]
    )
  )

@client.on(events.NewMessage(pattern="^/yardım$"))
async def help(event):
  helptext = "**#Nexus Tag Bot'un Kömək Menyusu**\n\nTag Etmək Üçün: /tag\nBaşqalarını qeyd etmək istədiyiniz mətnlə bu əmrdən istifadə edə bilərsiniz🤓\nMisal: `/tag Sabahınız Xeyir👻🤍`\nBu əmri istənilən mesaja cavab olaraq verə bilərsiniz. Bot istifadəçiləri həmin cavab mesajına işarələyəcək."
  await event.reply(
    helptext,
    link_preview=False,
    buttons=(
      [
        Button.url('💭 Gurup', 'https://t.me/iron_Blood_Gurup'),
        Button.url('🌐 Support', 'https://t.me/NEXUS_MMC')
      ]
    )
  )
  
@client.on(events.NewMessage(pattern="^/tag ?(.*)"))
async def mentionall(event):
  chat_id = event.chat_id
  if event.is_private:
    return await event.respond(" Bu əmr qruplarda və kanallarda istifadə edilə bilər!")
  
  is_admin = False
  try:
    partici_ = await client(GetParticipantRequest(
      event.chat_id,
      event.sender_id
    ))
  except UserNotParticipantError:
    is_admin = False
  else:
    if (
      isinstance(
        partici_.participant,
        (
          ChannelParticipantAdmin,
          ChannelParticipantCreator
        )
      )
    ):
      is_admin = True
  if not is_admin:
    return await event.respond("Yalnız adminlər hamısını qeyd edə bilər!")
  
  if event.pattern_match.group(1) and event.is_reply:
    return await event.respond("Mənə bir arqument verin!")
  elif event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.is_reply:
    mode = "text_on_reply"
    msg = await event.get_reply_message()
    if msg == None:
        return await event.respond("Köhnə mesajlar üçün üzvləri qeyd edə bilmərəm! (qrupa əlavə edilməzdən əvvəl göndərilən mesajlar)")
  else:
    return await event.respond("Mesajı cavablandırın və ya başqalarını qeyd etmək üçün mənə mətn yazın!")
  
  spam_chats.append(chat_id)
  usrnum = 0
  usrtxt = ''
  async for usr in client.iter_participants(chat_id):
    if not chat_id in spam_chats:
      break
    usrnum += 1
    usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
    if usrnum == 5:
      if mode == "text_on_cmd":
        txt = f"{usrtxt}\n\n{msg}"
        await client.send_message(chat_id, txt)
      elif mode == "text_on_reply":
        await msg.reply(usrtxt)
      await asyncio.sleep(2)
      usrnum = 0
      usrtxt = ''
  try:
    spam_chats.remove(chat_id)
  except:
    pass

@client.on(events.NewMessage(pattern="^/dur$"))
async def cancel_spam(event):
  if not event.chat_id in spam_chats:
    return await event.respond('Heç bir proses yoxdur...')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.respond('Dayandı🤓.')

print(">> BOT STARTED <<")
client.run_until_disconnected()
