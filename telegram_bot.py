from telegram import Update,ChatPermissions
from telegram.ext import Application, CommandHandler, MessageHandler, filters,CallbackContext
from telethon import TelegramClient
import datetime
import random
import json

with open("config.json") as config_file:
    config = json.load(config_file)

API_ID = config["API_ID"] # Your API_ID
HASH = config["HASH"] # Your APP_ID
TOKEN = config["TOKEN"]  # Reemplaza con el token de tu bot

async def start(update: Update, context):
    await update.message.reply_text("¡Hola! Soy un bot de prueba.")

async def admins(update: Update, context: CallbackContext):
    chat_id = update.effective_chat
    members = await context.bot.get_chat_administrators(chat_id.id)  # Obtiene administradores (pero no todos los usuarios)
    user_id = update.effective_user.id

    # Obtener la información del usuario en el chat
    chat_member = await context.bot.get_chat_member(chat_id, user_id)
    if chat_member.status in ["administrator", "creator"]:
        if not members:
            await update.message.reply_text("No pude obtener la lista de usuarios.")
            return

        mentions = []
        for member in members:
            user = member.user
            mentions.append(f"[{user.first_name}](tg://user?id={user.id})")  # Menciona por ID

        message_text = "📢 Mención general:\n" + " ".join(mentions)
        await update.message.reply_text(message_text, parse_mode="Markdown")

async def mute(update: Update, context: CallbackContext):
    """Mutea a un usuario mencionado o al usuario del mensaje respondido."""
    chat_id = update.effective_chat.id
    user_to_mute = None
    mute_time = 5  # Tiempo por defecto en minutos
    user_id = update.effective_user.id

    # Obtener la información del usuario en el chat
    chat_member = await context.bot.get_chat_member(chat_id, user_id)
    if chat_member.status in ["administrator", "creator"]:

        # Si se menciona con @usuario y se pasa un tiempo
        if context.args:
            if context.args[0].startswith("@"):  # Si el primer argumento es un @usuario
                username = context.args[0].lstrip("@")  # Quitar la @ para comparar
                try:
                    user_to_mute = await context.bot.get_chat_member(chat_id, username)
                except:
                    pass

                # Si hay un segundo argumento, intentamos convertirlo a minutos
                if len(context.args) > 1 and context.args[1].isdigit():
                    mute_time = int(context.args[1])

            # Si no se menciona un @usuario pero hay un número, es el tiempo del muteo
            elif context.args[0].isdigit():
                mute_time = int(context.args[0])

        # Si no se mencionó un usuario, revisamos si se respondió a un mensaje
        if not user_to_mute and update.message.reply_to_message:
            user_to_mute = update.message.reply_to_message.from_user

        if not user_to_mute:
            await update.message.reply_text("No encontré a ese usuario en el grupo o no tengo permisos.")
            return

        # Configurar permisos para mutear (sin hablar ni enviar multimedia)
        permissions = ChatPermissions(
            can_send_messages=False,
            can_send_audios=False,
            can_send_documents=False,
            can_send_photos=False,
            can_send_videos=False,
            can_send_video_notes=False,
            can_send_voice_notes=False,
            can_send_polls=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False
        )

        # Duración del muteo (según los minutos indicados)
        until_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=mute_time)
        await context.bot.restrict_chat_member(chat_id, user_to_mute.id, permissions, until_date)

        await update.message.reply_text(f"🔇 @{user_to_mute.username} ha sido muteado por {mute_time} minutos.")
    else:
        return
async def unmute(update: Update, context: CallbackContext):
    """Desmutea a un usuario mencionado o al usuario del mensaje respondido."""
    chat_id = update.effective_chat.id
    user_to_unmute = None
    user_id = update.effective_user.id

    # Obtener la información del usuario en el chat
    chat_member = await context.bot.get_chat_member(chat_id, user_id)
    if chat_member.status in ["administrator", "creator"]:
        # Si se menciona con @usuario
        if context.args:
            if context.args[0].startswith("@"):
                username = context.args[0].lstrip("@")
                try:
                    user_to_unmute = await context.bot.get_chat_member(chat_id, username)
                except:
                    pass

        # Si no se mencionó un usuario, revisamos si se respondió a un mensaje
        if not user_to_unmute and update.message.reply_to_message:
            user_to_unmute = update.message.reply_to_message.from_user

        if not user_to_unmute:
            await update.message.reply_text("No encontré a ese usuario en el grupo o no tengo permisos.")
            return

        # Restaurar los permisos a los predeterminados (sin restricciones)
        permissions = ChatPermissions(
            can_send_messages=True,
            can_send_audios=True,
            can_send_documents=True,
            can_send_photos=True,
            can_send_videos=True,
            can_send_video_notes=True,
            can_send_voice_notes=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )
        

        await context.bot.restrict_chat_member(chat_id, user_to_unmute.id, permissions)
    
        await update.message.reply_text(f"🔊 @{user_to_unmute.username} ha sido desmuteado.")
    else:
        return

async def welcome(update: Update, context: CallbackContext):
    """Cuando un nuevo miembro se une al grupo, el bot lo saluda."""
    # Verificar si hay nuevos miembros
    for new_member in update.message.new_chat_members:
        # Enviar mensaje de bienvenida
        welcome_message = f"¡Bienvenid@ al grupo, {new_member.full_name}! 🎉"
        await update.message.reply_text(welcome_message)

async def size(update: Update, context: CallbackContext):
    """Responde con un número aleatorio entre 1 y 47 con el nombre del usuario."""
    user_name = update.message.from_user.first_name  # Obtener el nombre del usuario
    random_size = random.randint(1, 47)  # Número aleatorio entre 1 y 47
    response = f"{user_name}, el tamaño de tu 🍆 es de {random_size} cm. 😉"
    await update.message.reply_text(response)

async def  rol_dice(update: Update, context: CallbackContext):
    """Responde con un número aleatorio entre 1 y 47 con el nombre del usuario."""
    user_name = update.message.from_user.first_name  # Obtener el nombre del usuario
    random_dice = random.randint(1, 6)  # Número aleatorio entre 1 y 6
    dice = "🎲"  # Emoji del dado
    if random_dice ==1:
        dice = "1️⃣"
    if random_dice ==2:
        dice = "2️⃣"
    if random_dice ==3:
        dice = "3️⃣"
    if random_dice ==4:
        dice = "4️⃣"
    if random_dice ==5:
        dice = "5️⃣"
    if random_dice ==6:
        dice = "6️⃣"
    response = f"{user_name}, ha sacado {dice} en el dado. 🎲"
    await update.message.reply_text(response)

async def assign_admin(update: Update, context: CallbackContext):
    """Asigna el rol de admin a un usuario mencionado."""
    chat_id = update.effective_chat.id
    user_to_promote = None
    user_id = update.effective_user.id

    # Obtener la información del usuario en el chat
    chat_member = await context.bot.get_chat_member(chat_id, user_id)
    if chat_member.status in ["creator"]:
        # Verificar si se responde a un mensaje o si se menciona a un usuario
        try:
            # Obtener el miembro del chat por su nombre de usuario
            user_to_promote = update.message.reply_to_message.from_user
        except:
            await update.message.reply_text("No encontré ese usuario en el grupo.")
            return

        # Verificar si el bot tiene permisos para promover a admin
        bot_member = await context.bot.get_chat_member(chat_id, context.bot.id)
        if bot_member.status != "administrator":
            await update.message.reply_text("El bot necesita ser administrador para hacer esto.")
            return

        # Asignar el rol de administrador
        try:
            await context.bot.promote_chat_member(chat_id, user_to_promote.id, can_change_info=True, can_post_messages=True,
                                                  can_edit_messages=True, can_delete_messages=True, can_invite_users=True,
                                                  can_pin_messages=True, can_promote_members=True)
            await update.message.reply_text(f"¡{user_to_promote.username} ahora es un administrador del grupo! 🎉")
        except Exception as e:
            await update.message.reply_text(f"Hubo un error al asignar el rol de administrador: {e}")

async def get_users(client, group_id):
    user_names = []  # Lista para almacenar los nombres
    async for user in client.iter_participants(group_id):
        if user.id:  # Verifica que tenga un nombre
            #print(user)  # Imprime el nombre
            user_names.append(user.id)

    print("Lista de nombres:", user_names)  # Imprime la lista
    return user_names

bot = TelegramClient('bot', API_ID, HASH).start(bot_token=TOKEN)

async def get_group_id(update: Update, context: CallbackContext):
    """Obtiene el ID del grupo donde se ejecuta el comando."""
    chat_id = update.effective_chat.id
    return chat_id

async def all(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Obtener la información del usuario en el chat
    chat_member = await context.bot.get_chat_member(chat_id, user_id)
    print(chat_member.status)
    if chat_member.status in ["administrator", "creator"]:
        async with bot:
            group_id = await get_group_id(update,context)
            list_user_ids = await get_users(bot,group_id )
        # Lista de textos o emojis aleatorios
        random_texts = [
        "😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "🥲", "☺️",  # Caritas felices
        "😊", "😇", "🙂", "🙃", "😉", "😌", "😍", "😘", "😗", "😙",  # Caritas con amor
        "😚", "😋", "😜", "😝", "😛", "🤑", "🤗", "🤭", "🤫", "🤔",  # Expresiones variadas
        "🤐", "🤨", "😐", "😑", "😶", "😏", "😒", "🙄", "😬", "🤥",  # Caritas con actitud
        "😪", "😴", "🤤", "😷", "🤒", "🤕", "🤢", "🤮", "🤧", "🥵",  # Enfermedades y clima
        "🥶", "🥴", "😵", "🤯", "🤠", "🥳", "🥸", "😎", "🤓", "🧐"   # Diversión y estilos
]   

        # Generar el mensaje con un texto o emoji aleatorio
        response = "All:"+ ",".join([f"<a href='tg://user?id={user_id}'>{random.choice(random_texts)}</a>" for user_id in list_user_ids])
        await update.message.reply_html(response)
    else:
        return


def main():
    app = Application.builder().token(TOKEN).build()
    

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admins", admins)) #admins
    app.add_handler(CommandHandler("mute", mute)) #admins
    app.add_handler(CommandHandler("unmute", unmute)) #admins
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(CommandHandler("size", size)) #all
    app.add_handler(CommandHandler("admin", assign_admin)) #creador
    app.add_handler(CommandHandler("dice", rol_dice))#all
    app.add_handler(CommandHandler("getid", get_group_id))#creador
    app.add_handler(CommandHandler("all", all))#admins

    print("Bot en marcha...")
    app.run_polling()

if __name__ == "__main__":
    main()