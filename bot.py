import logging
import json
import re
import os
from datetime import datetime
from typing import Final
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, filters, ContextTypes

BOT_USERNAME: Final = '@Mochichatbot_Bot'

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

with open('menu.json', 'r', encoding='utf-8') as f:
    menu_data = json.load(f)

def get_name(index: int) -> str:
    try:
        postre = menu_data['postres'][index]
        name = f"{postre['nombre']}"
        return name
    except IndexError:
        return "Opcion no valida."

def get_food_description(index: int) -> str:
    try:
        postre = menu_data['postres'][index]
        descripcion = f"Descripcion: {postre['descripcion']}\nPrecio: ${postre['precio']} Pesos"
        return descripcion
    except IndexError:
        return ""

def get_food_image(index: int) -> str:
    try:
        postre = menu_data['postres'][index]
        return postre['img']
    except IndexError:
        return ""

# Funcion para mostrar el menu
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    await show_menu(update.message, context, user_id)

async def show_menu(update, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> None:
    keyboard = [
        [InlineKeyboardButton(get_name(i * 2), callback_data=str(i * 2)),
         InlineKeyboardButton(get_name(i * 2 + 1), callback_data=str(i * 2 + 1))]
        for i in range((len(menu_data['postres']) + 1) // 2)
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.reply_text("Por favor elija una opcion para describir el alimento:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    index = int(query.data)
    await query.answer()

    description = get_food_description(index)
    image_url = get_food_image(index)

    if image_url:
        await query.message.reply_photo(photo=open(image_url, 'rb'), caption=description)
    else:
        await query.edit_message_text(text=description)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("/menu para conocer el menu.")

# Funcion para extraer las ordenes del mensaje de texto
def extract_orders(text: str) -> list:
    food_names = [postre['nombre'].lower() for postre in menu_data['postres']]
    pattern = re.compile(r'(\d+)\s+(' + '|'.join(re.escape(name) for name in food_names) + r')', re.IGNORECASE)
    matches = pattern.findall(text)
    return [(int(quantity), name.lower()) for quantity, name in matches]

# Funcion para guardar la orden
def save_order(username: str, orders: list) -> None:
    now = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
    order_data = {
        'usuario': username,
        'fecha': now,
        'orden': [{'cantidad': quantity, 'producto': name} for quantity, name in orders]
    }
    os.makedirs('ordenes', exist_ok=True)
    filename = f'{username}_{now}.json'
    file_path = os.path.join('ordenes', filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(order_data, f, ensure_ascii=False, indent=4)
    logger.info(f"Orden guardada en {file_path}")

# Funcion para manejar las respuestas del usuario
async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str) -> None:
    processed: str = text.lower()

    if 'hola' in processed or 'saludos' in processed:
        await update.message.reply_text('¡Hola! ¿En que puedo ayudarte?')
        
    elif 'menu' in processed:
        await menu(update, context)

    elif 'gracias' in processed:
        await update.message.reply_text('¡Gracias por tu visita!')

    elif 'orden' in processed or 'ordenar' in processed:
        message = 'Claro! ¿Qué le gustaría ordenar?:\n\n'
        for postre in menu_data['postres']:
            message += f"{postre['nombre']} - [ ${postre['precio']} ]\n"
        await update.message.reply_text(message)
    else:
        orders = extract_orders(processed)
        if orders:
            username = update.message.from_user.username or update.message.from_user.full_name
            logger.info(f"Orden recibida de {username}: {orders}")
            save_order(username, orders)
            response = "Se ha registrado tu orden:\n" + "\n".join([f"{quantity} x {name}" for quantity, name in orders])
            await update.message.reply_text(response)
        else:
            await update.message.reply_text('Lo siento, no entendi tu mensaje. ¿Podrias reformularlo?')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(f'user({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            await handle_response(update, context, new_text)
        else:
            return
    else:
        await handle_response(update, context, text)

def main() -> None:
    application = Application.builder().token("7193336435:AAFL7za4D1CY_RXeK2cC32GFFX-h4OIvyNY").build()

    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CommandHandler("help", help_command))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
