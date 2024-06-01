# Mochichatbot

Mochichatbot es un bot de Telegram diseñado para mostrar un menú de postres y manejar ordenes de usuarios. El bot permite a los usuarios interactuar con un menu, ver descripciones y precios de los postres, y hacer ordenes que se guardan en archivos JSON.
Las preguntas comunes a escribir son:
"Que hay en el menu?"
"Me gustaria hacer una orden"


## Caracteristicas

- **Mostrar menu**: El bot muestra un menu interactivo de postres.
                    para esto solo se debe de preguntar por el menu.
                    Ejemplo: "Me gustaria ver el menu"

- **Descripciones y precios**: Los usuarios pueden ver descripciones y precios de los postres.
                               Al seleccionar una opcion, el bot muestrea la descripcion, imagen y precio del postre seleccionado.

- **Realizar ordenes**: Los usuarios pueden realizar ordenes escribiendo mensajes que describan su pedido.

- **Guardar ordenes**: Las ordenes se guardan en archivos JSON dentro de una carpeta para su posterior revision.

## Requisitos

- Python 3.8 o superior
- Paquetes de Python:
  - `python-telegram-bot`
  - `logging`
  - `json`
  - `re`
  - `os`
  - `datetime`
  - `typing`


Mapa:

# Importaciones
import logging
import json
import re
import os
from datetime import datetime
from typing import Final
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, filters, ContextTypes

BOT_USERNAME: Final = '@Mochichatbot_Bot'

# Configuracion del registro de eventos
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

# Carga de datos del menu desde un archivo JSON
with open('menu.json', 'r', encoding='utf-8') as f:
    menu_data = json.load(f)

# Funciones para obtener informacion del menu
def get_name(index: int) -> str:
...

def get_food_description(index: int) -> str:
...

def get_food_image(index: int) -> str:
...

# Funcion para mostrar el menu
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
...

async def show_menu(update, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> None:
...

# Funcion para manejar los botones de seleccion de alimentos
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
...

# Funcion para mostrar el comando de ayuda
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
...

# Funcion para extraer ordenes del mensaje de texto
def extract_orders(text: str) -> list:
...

# Funcion para guardar la orden en un archivo JSON
def save_order(username: str, orders: list) -> None:
...

# Funcion para manejar las respuestas del usuario
async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str) -> None:
...

# Funcion para manejar los mensajes recibidos
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
...

# Funcion principal
def main() -> None:
...
