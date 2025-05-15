import telebot
import random
import string
import json
import os
from datetime import datetime, timedelta

# Reemplaza esto con tu token de bot de Telegram
# Obtenlo de @BotFather en Telegram
BOT_TOKEN = "7912969152:AAFaIvqm39uPL2C7PXS2xInVITo-TwZ_F-8"

# Inicializar el bot
bot = telebot.TeleBot(BOT_TOKEN)

# Archivo para almacenar las claves
KEYS_FILE = "access_keys.json"

# Función para cargar las claves existentes
def load_keys():
    if os.path.exists(KEYS_FILE):
        with open(KEYS_FILE, 'r') as f:
            try:
                return json.load(f)
            except:
                return {"keys": {}}
    else:
        return {"keys": {}}

# Función para guardar las claves
def save_keys(keys_data):
    with open(KEYS_FILE, 'w') as f:
        json.dump(keys_data, f, indent=4)

# Función para generar una clave única
def generate_key(length=16):
    characters = string.ascii_letters + string.digits
    key = ''.join(random.choice(characters) for _ in range(length))
    return key

# Manejador para el comando /start
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, 
                f"👋 Hola {message.from_user.first_name}!\n\n"
                f"Este es el bot oficial de generación de claves para Leunam CPM Tool.\n\n"
                f"Usa /help para ver los comandos disponibles.")

# Manejador para el comando /help
@bot.message_handler(commands=['help'])
def help_command(message):
    user_id = message.from_user.id
    help_text = (
        "📜 *Comandos disponibles*:\n\n"
        "/generar - Generar una nueva clave de acceso\n"
        "/miscaves - Ver tus claves activas\n"
        "/revocar {clave} - Revocar una clave específica\n\n"
    )
    
    # Añadir comandos de administrador si el usuario es admin
    if user_id in ADMIN_IDS:
        help_text += (
            "🔐 *Comandos de administrador*:\n\n"
            "/admin_generar {telegram_id} {días} {coins} - Generar clave para un usuario\n"
            "/admin_generar_permanente {telegram_id} - Generar clave permanente con saldo ilimitado\n"
            "/admin_listar - Listar todas las claves\n"
        )
    
    bot.reply_to(message, help_text, parse_mode="Markdown")

# Lista de IDs de administradores autorizados
ADMIN_IDS = [
    7869356178
]

# Manejador para generar clave para usuarios normales
@bot.message_handler(commands=['generar'])
def generate_key_command(message):
    user_id = message.from_user.id
    keys_data = load_keys()
    
    # Verificar si el usuario ya tiene una clave
    user_keys = [k for k, v in keys_data["keys"].items() if v["telegram_id"] == user_id]
    
    if user_keys and len(user_keys) >= 1:
        bot.reply_to(message, "❌ Ya tienes una clave activa. Usa /miscaves para verla.")
        return
    
    # Generar nueva clave
    new_key = generate_key()
    expiry_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
    
    # Guardar la clave
    keys_data["keys"][new_key] = {
        "telegram_id": user_id,
        "username": message.from_user.username or "Unknown",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "expires_at": expiry_date,
        "coins": 20000,  # Créditos iniciales
        "is_unlimited": False
    }
    
    save_keys(keys_data)
    
    bot.reply_to(message, 
                f"✅ *Clave generada exitosamente*\n\n"
                f"🔑 `{new_key}`\n\n"
                f"📊 Créditos: 20,000\n"
                f"⏱ Expira: {expiry_date}\n\n"
                f"_No compartas esta clave con nadie._", 
                parse_mode="Markdown")

# Manejador para ver claves propias
@bot.message_handler(commands=['miscaves'])
def my_keys_command(message):
    user_id = message.from_user.id
    keys_data = load_keys()
    
    user_keys = {k: v for k, v in keys_data["keys"].items() if v["telegram_id"] == user_id}
    
    if not user_keys:
        bot.reply_to(message, "❌ No tienes claves activas. Usa /generar para crear una.")
        return
    
    reply = "🔑 *Tus claves activas*:\n\n"
    
    for key, data in user_keys.items():
        reply += f"Clave: `{key}`\n"
        
        if data.get('is_unlimited', False):
            reply += f"Créditos: Ilimitado\n"
        else:
            reply += f"Créditos: {data['coins']}\n"
            
        if data.get('permanent', False):
            reply += f"Validez: Permanente\n"
        else:
            reply += f"Expira: {data['expires_at']}\n"
        
        reply += "\n"
    
    bot.reply_to(message, reply, parse_mode="Markdown")

# Manejador para revocar una clave
@bot.message_handler(commands=['revocar'])
def revoke_key_command(message):
    user_id = message.from_user.id
    args = message.text.split()
    
    if len(args) != 2:
        bot.reply_to(message, "❌ Uso correcto: /revocar {clave}")
        return
    
    key_to_revoke = args[1]
    keys_data = load_keys()
    
    if key_to_revoke not in keys_data["keys"]:
        bot.reply_to(message, "❌ Clave no encontrada.")
        return
    
    if keys_data["keys"][key_to_revoke]["telegram_id"] != user_id and user_id not in ADMIN_IDS:
        bot.reply_to(message, "❌ No tienes permiso para revocar esta clave.")
        return
    
    # Revocar la clave
    del keys_data["keys"][key_to_revoke]
    save_keys(keys_data)
    
    bot.reply_to(message, f"✅ Clave `{key_to_revoke}` revocada exitosamente.", parse_mode="Markdown")

# Manejador para generar clave (solo administradores)
@bot.message_handler(commands=['admin_generar'])
def admin_generate_key_command(message):
    user_id = message.from_user.id
    
    if user_id not in ADMIN_IDS:
        bot.reply_to(message, "❌ No tienes permisos de administrador.")
        return
    
    args = message.text.split()
    
    if len(args) != 4:
        bot.reply_to(message, "❌ Uso correcto: /admin_generar {telegram_id} {días} {coins}")
        return
    
    try:
        target_user_id = int(args[1])
        days = int(args[2])
        coins = int(args[3])
    except ValueError:
        bot.reply_to(message, "❌ Formato inválido. Usa números para telegram_id, días y coins.")
        return
    
    # Generar nueva clave
    new_key = generate_key()
    expiry_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
    
    # Guardar la clave
    keys_data = load_keys()
    keys_data["keys"][new_key] = {
        "telegram_id": target_user_id,
        "username": "Admin Generated",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "expires_at": expiry_date,
        "coins": coins,
        "is_unlimited": coins == -1,
        "permanent": False
    }
    
    save_keys(keys_data)
    
    # Notificar al administrador
    bot.reply_to(message, 
                f"✅ *Clave generada exitosamente para usuario {target_user_id}*\n\n"
                f"🔑 `{new_key}`\n\n"
                f"📊 Créditos: {coins if coins != -1 else 'Ilimitado'}\n"
                f"⏱ Expira en: {days} días\n", 
                parse_mode="Markdown")
    
    # Intentar notificar al usuario
    try:
        bot.send_message(target_user_id, 
                        f"✅ *Has recibido una nueva clave de acceso*\n\n"
                        f"🔑 `{new_key}`\n\n"
                        f"📊 Créditos: {coins if coins != -1 else 'Ilimitado'}\n"
                        f"⏱ Expira: {expiry_date}\n\n"
                        f"_No compartas esta clave con nadie._", 
                        parse_mode="Markdown")
    except:
        bot.reply_to(message, "⚠️ No se pudo notificar al usuario. Asegúrate de que haya iniciado el bot.")

# Nuevo manejador para generar clave permanente con saldo ilimitado (solo administradores)
@bot.message_handler(commands=['admin_generar_permanente'])
def admin_generate_permanent_key_command(message):
    user_id = message.from_user.id
    
    if user_id not in ADMIN_IDS:
        bot.reply_to(message, "❌ No tienes permisos de administrador.")
        return
    
    args = message.text.split()
    
    if len(args) != 2:
        bot.reply_to(message, "❌ Uso correcto: /admin_generar_permanente {telegram_id}")
        return
    
    try:
        target_user_id = int(args[1])
    except ValueError:
        bot.reply_to(message, "❌ Formato inválido. Usa un número para telegram_id.")
        return
    
    # Generar nueva clave permanente
    new_key = generate_key()
    
    # Guardar la clave como permanente y con créditos ilimitados
    keys_data = load_keys()
    keys_data["keys"][new_key] = {
        "telegram_id": target_user_id,
        "username": "Admin Generated",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "expires_at": "Permanente",
        "coins": -1,  # -1 indica créditos ilimitados
        "is_unlimited": True,
        "permanent": True
    }
    
    save_keys(keys_data)
    
    # Notificar al administrador
    bot.reply_to(message, 
                f"✅ *Clave permanente generada exitosamente para usuario {target_user_id}*\n\n"
                f"🔑 `{new_key}`\n\n"
                f"📊 Créditos: Ilimitado\n"
                f"⏱ Validez: Permanente\n", 
                parse_mode="Markdown")
    
    # Intentar notificar al usuario
    try:
        bot.send_message(target_user_id, 
                        f"✅ *Has recibido una nueva clave de acceso permanente*\n\n"
                        f"🔑 `{new_key}`\n\n"
                        f"📊 Créditos: Ilimitado\n"
                        f"⏱ Validez: Permanente\n\n"
                        f"_No compartas esta clave con nadie._", 
                        parse_mode="Markdown")
    except:
        bot.reply_to(message, "⚠️ No se pudo notificar al usuario. Asegúrate de que haya iniciado el bot.")

# Manejador para listar todas las claves (solo administradores)
@bot.message_handler(commands=['admin_listar'])
def admin_list_keys_command(message):
    user_id = message.from_user.id
    
    if user_id not in ADMIN_IDS:
        bot.reply_to(message, "❌ No tienes permisos de administrador.")
        return
    
    keys_data = load_keys()
    
    if not keys_data["keys"]:
        bot.reply_to(message, "No hay claves generadas.")
        return
    
    reply = "🔑 *Todas las claves*:\n\n"
    
    for key, data in keys_data["keys"].items():
        reply += f"Clave: `{key}`\n"
        reply += f"Usuario: {data['telegram_id']} (@{data['username']})\n"
        
        if data.get('is_unlimited', False):
            reply += f"Créditos: Ilimitado\n"
        else:
            reply += f"Créditos: {data['coins']}\n"
            
        reply += f"Creada: {data['created_at']}\n"
        
        if data.get('permanent', False):
            reply += f"Validez: Permanente\n"
        else:
            reply += f"Expira: {data['expires_at']}\n"
            
        reply += "\n"
        
        # Telegram tiene un límite de 4096 caracteres por mensaje
        if len(reply) > 3500:
            bot.reply_to(message, reply, parse_mode="Markdown")
            reply = "Continuación...\n\n"
    
    if reply:
        bot.reply_to(message, reply, parse_mode="Markdown")

# Manejador para verificar estado de una clave específica
@bot.message_handler(func=lambda message: message.text and len(message.text) >= 10 and not message.text.startswith('/'))
def check_key_status(message):
    potential_key = message.text.strip()
    keys_data = load_keys()
    
    if potential_key in keys_data["keys"]:
        key_data = keys_data["keys"][potential_key]
        
        # Verificar si la clave ha expirado (a menos que sea permanente)
        if not key_data.get('permanent', False):
            expiry_date = datetime.strptime(key_data["expires_at"], "%Y-%m-%d %H:%M:%S")
            if expiry_date < datetime.now():
                bot.reply_to(message, "❌ Esta clave ha expirado.")
                return
        
        # Preparar mensaje sobre los créditos
        credits_info = "Ilimitado" if key_data.get('is_unlimited', False) else key_data['coins']
        
        # Preparar mensaje sobre la expiración
        expiry_info = "Permanente" if key_data.get('permanent', False) else key_data['expires_at']
        
        bot.reply_to(message, 
                    f"✅ *Información de la clave*\n\n"
                    f"🔑 `{potential_key}`\n\n"
                    f"📊 Créditos: {credits_info}\n"
                    f"⏱ Validez: {expiry_info}\n", 
                    parse_mode="Markdown")
    
# Iniciar el bot
if __name__ == "__main__":
    print("Bot iniciado. Presiona Ctrl+C para detener.")
    bot.polling(none_stop=True)