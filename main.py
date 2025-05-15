from pystyle import Box, Colors, Colorate
import random
import requests
from time import sleep
import os
import signal
import sys
from pyfiglet import figlet_format
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich.style import Style
import json
import logging

# Importamos el módulo actualizado
from leunamcpm import leunamcpm

# Configuración del logging
logging.basicConfig(
    filename='leunam_app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("leunam_app")

# Información de contacto
__CHANNEL_USERNAME__ = "Leunam0802"
__GROUP_USERNAME__   = "https://t.me/+JDaiBsc8CQUxODQ5"
__VERSION__ = "1.2.0"

def check_exit():
    """Pregunta al usuario si desea salir"""
    answ = Prompt.ask("[?] ¿Quieres salir?", choices=["y", "n"], default="n")
    if answ.lower() == "y":
        print(Colorate.Horizontal(Colors.rainbow, f'Gracias por usar nuestra herramienta, únete a nuestro canal de telegram: @{__CHANNEL_USERNAME__}.'))
        sys.exit(0)

def signal_handler(sig, frame):
    """Maneja la señal CTRL+C"""
    print("\n Adiós...")
    sys.exit(0)

def gradient_text(text, colors):
    """Crea texto con degradado de colores"""
    lines = text.splitlines()
    height = len(lines)
    width = max(len(line) for line in lines)
    colorful_text = Text()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != ' ':
                color_index = int(((x / (width - 1 if width > 1 else 1)) + (y / (height - 1 if height > 1 else 1))) * 0.5 * (len(colors) - 1))
                color_index = min(max(color_index, 0), len(colors) - 1)  # Ensure the index is within bounds
                style = Style(color=colors[color_index])
                colorful_text.append(char, style=style)
            else:
                colorful_text.append(char)
        colorful_text.append("\n")
    return colorful_text

def banner(console):
    """Muestra el banner principal de la aplicación"""
    os.system('cls' if os.name == 'nt' else 'clear')
    # Banner principal
    brand_name = figlet_format('Leunam', font='starwars')  
    colors = [
        "rgb(255,0,0)", "rgb(255,69,0)", "rgb(255,140,0)", "rgb(255,215,0)", "rgb(173,255,47)", 
    ]
    colorful_text = gradient_text(brand_name, colors)
    console.print(colorful_text)
    print(Colorate.Horizontal(Colors.rainbow, '============================================================'))
    print(Colorate.Horizontal(Colors.rainbow, '\t         POR FAVOR CIERRA SESIÓN EN CPM ANTES DE USAR ESTA HERRAMIENTA'))
    print(Colorate.Horizontal(Colors.rainbow, '    COMPARTIR LA CLAVE DE ACCESO NO ESTÁ PERMITIDO Y SERÁ BLOQUEADO'))
    print(Colorate.Horizontal(Colors.rainbow, f' ‌           Telegram: @{__CHANNEL_USERNAME__} | {__GROUP_USERNAME__}'))
    print(Colorate.Horizontal(Colors.rainbow, f' ‌           Versión: {__VERSION__}'))
    print(Colorate.Horizontal(Colors.rainbow, '============================================================'))

def load_player_data(cpm, console):
    """Carga y muestra los datos del jugador"""
    try:
        console.print("[bold cyan][%] Obteniendo datos del jugador...[/bold cyan]")
        response = cpm.get_player_data()
        if response.get('ok'):
            data = response.get('data')
            if data and 'floats' in data and 'localID' in data and 'money' in data and 'coin' in data:
                print(Colorate.Horizontal(Colors.rainbow, '==========[ DETALLES DEL JUGADOR ]=========='))
                print(Colorate.Horizontal(Colors.rainbow, f'Nombre   : {(data.get("Name") if "Name" in data else "INDEFINIDO")}.'))
                print(Colorate.Horizontal(Colors.rainbow, f'LocalID  : {data.get("localID")}.'))
                print(Colorate.Horizontal(Colors.rainbow, f'Dinero   : {data.get("money")}.'))
                print(Colorate.Horizontal(Colors.rainbow, f'Monedas  : {data.get("coin")}.'))
                return True
            else:
                print(Colorate.Horizontal(Colors.rainbow, '! ERROR: Las cuentas nuevas deben iniciar sesión en el juego al menos una vez !'))
                sleep(2)
                return False
        else:
            print(Colorate.Horizontal(Colors.rainbow, f'! ERROR: {response.get("message", "Sesión no válida")} !'))
            sleep(2)
            return False
    except Exception as e:
        logger.error(f"Error al cargar datos del jugador: {e}")
        print(Colorate.Horizontal(Colors.rainbow, f'! ERROR: {str(e)} !'))
        sleep(2)
        return False

def load_key_data(cpm, console):
    """Carga y muestra los datos de la clave de acceso"""
    try:
        console.print("[bold cyan][%] Obteniendo datos de la clave...[/bold cyan]")
        data = cpm.get_key_data()
        
        if data:
            print(Colorate.Horizontal(Colors.rainbow, '========[ DETALLES DE CLAVE DE ACCESO ]========'))
            print(Colorate.Horizontal(Colors.rainbow, f'Clave de acceso : {data.get("access_key", "No disponible")}.'))
            print(Colorate.Horizontal(Colors.rainbow, f'ID de Telegram  : {data.get("telegram_id", "No disponible")}.'))
            print(Colorate.Horizontal(Colors.rainbow, f'Saldo $         : {(data.get("coins", "0") if not data.get("is_unlimited", False) else "Ilimitado")}.'))
            return True
        else:
            print(Colorate.Horizontal(Colors.rainbow, '! ERROR: No se pudieron obtener datos de la clave !'))
            sleep(2)
            return False
    except Exception as e:
        logger.error(f"Error al cargar datos de la clave: {e}")
        print(Colorate.Horizontal(Colors.rainbow, f'! ERROR: {str(e)} !'))
        sleep(2)
        return False

def prompt_valid_value(content, tag, password=False):
    """Solicita y valida un valor de entrada"""
    while True:
        value = Prompt.ask(content, password=password)
        if not value or value.isspace():
            print(Colorate.Horizontal(Colors.rainbow, f'{tag} no puede estar vacío o solo espacios. Por favor intente nuevamente.'))
        else:
            return value
            
def load_client_details(console):
    """Carga y muestra la información de ubicación del cliente"""
    try:
        console.print("[bold cyan][%] Detectando ubicación...[/bold cyan]")
        response = requests.get("http://ip-api.com/json", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(Colorate.Horizontal(Colors.rainbow, '=============[ UBICACIÓN ]============='))
            print(Colorate.Horizontal(Colors.rainbow, f'Dirección IP : {data.get("query", "No disponible")}.'))
            print(Colorate.Horizontal(Colors.rainbow, f'Ubicación    : {data.get("city", "N/A")} {data.get("regionName", "N/A")} {data.get("countryCode", "N/A")}.'))
            print(Colorate.Horizontal(Colors.rainbow, f'País         : {data.get("country", "N/A")} {data.get("zip", "N/A")}.'))
            print(Colorate.Horizontal(Colors.rainbow, '===============[ MENÚ ]==============='))
        else:
            print(Colorate.Horizontal(Colors.rainbow, '=============[ UBICACIÓN ]============='))
            print(Colorate.Horizontal(Colors.rainbow, 'No se pudo detectar la ubicación.'))
            print(Colorate.Horizontal(Colors.rainbow, '===============[ MENÚ ]==============='))
    except Exception as e:
        logger.error(f"Error al obtener ubicación: {e}")
        print(Colorate.Horizontal(Colors.rainbow, '=============[ UBICACIÓN ]============='))
        print(Colorate.Horizontal(Colors.rainbow, 'No se pudo detectar la ubicación.'))
        print(Colorate.Horizontal(Colors.rainbow, '===============[ MENÚ ]==============='))

def interpolate_color(start_color, end_color, fraction):
    """Interpola entre dos colores para un gradiente"""
    try:
        start_rgb = tuple(int(start_color[i:i+2], 16) for i in (1, 3, 5))
        end_rgb = tuple(int(end_color[i:i+2], 16) for i in (1, 3, 5))
        interpolated_rgb = tuple(int(start + fraction * (end - start)) for start, end in zip(start_rgb, end_rgb))
        return "{:02x}{:02x}{:02x}".format(*interpolated_rgb)
    except Exception as e:
        logger.error(f"Error en interpolate_color: {e}")
        return "ffffff"  # Color blanco por defecto en caso de error

def rainbow_gradient_string(customer_name):
    """Crea un string con gradiente arcoíris"""
    try:
        modified_string = ""
        num_chars = len(customer_name)
        start_color = "#" + "{:06x}".format(random.randint(0, 0xFFFFFF))
        end_color = "#" + "{:06x}".format(random.randint(0, 0xFFFFFF))
        for i, char in enumerate(customer_name):
            fraction = i / max(num_chars - 1, 1)
            interpolated_color = interpolate_color(start_color, end_color, fraction)
            modified_string += f'[#{interpolated_color}]{char}'
        return modified_string
    except Exception as e:
        logger.error(f"Error en rainbow_gradient_string: {e}")
        return customer_name  # Devolver el nombre original en caso de error

def modificar_todos_los_autos(cpm, hp, hp_interno, nm, torque, console):
    """Modifica todos los autos con los parámetros especificados"""
    try:
        console.print("[bold cyan][%] Modificando todos los autos...[/bold cyan]")
        response = cpm.modificar_todos_los_autos(hp, hp_interno, nm, torque)
        if response:
            print(Colorate.Horizontal(Colors.rainbow, 'Todos los autos han sido modificados exitosamente.'))
            return True
        else:
            print(Colorate.Horizontal(Colors.rainbow, 'Error al modificar los autos.'))
            return False
    except Exception as e:
        logger.error(f"Error al modificar autos: {e}")
        print(Colorate.Horizontal(Colors.rainbow, f'Error: {e}'))
        return False

def mostrar_menu_servicios():
    """Muestra el menú de servicios disponibles"""
    print(Colorate.Horizontal(Colors.rainbow, '{01}: Aumentar dinero                   1.500'))
    print(Colorate.Horizontal(Colors.rainbow, '{02}: Aumentar monedas                  4.500'))
    print(Colorate.Horizontal(Colors.rainbow, '{03}: Rango Rey                         8.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{04}: Cambiar ID                        4.500'))
    print(Colorate.Horizontal(Colors.rainbow, '{05}: Cambiar nombre                    100'))
    print(Colorate.Horizontal(Colors.rainbow, '{06}: Cambiar nombre (Arcoíris)         100'))
    print(Colorate.Horizontal(Colors.rainbow, '{07}: Placas de número                  2.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{08}: Eliminar cuenta                   GRATIS'))
    print(Colorate.Horizontal(Colors.rainbow, '{09}: Registrar cuenta                  GRATIS'))
    print(Colorate.Horizontal(Colors.rainbow, '{10}: Eliminar amigos                   500'))
    print(Colorate.Horizontal(Colors.rainbow, '{11}: Desbloquear autos pagados         5.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{12}: Desbloquear todos los autos       6.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{13}: Desbloquear sirenas de autos      3.500'))
    print(Colorate.Horizontal(Colors.rainbow, '{14}: Desbloquear motor w16             4.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{15}: Desbloquear todas las bocinas     3.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{16}: Desbloquear sin daños             3.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{17}: Desbloquear combustible ilimitado 3.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{18}: Desbloquear Casa 3                4.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{19}: Desbloquear humo                  4.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{20}: Desbloquear llantas               4.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{21}: Desbloquear animaciones           2.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{22}: Desbloquear equipos M             3.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{23}: Desbloquear equipos F             3.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{24}: Cambiar carreras ganadas          1.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{25}: Cambiar carreras perdidas         1.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{26}: Clonar cuenta                     7.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{27}: HP personalizado                  2.500'))
    print(Colorate.Horizontal(Colors.rainbow, '{28}: Ángulo personalizado              1.500'))
    print(Colorate.Horizontal(Colors.rainbow, '{29}: Quemado de llantas personalizado  1.500'))
    print(Colorate.Horizontal(Colors.rainbow, '{30}: Kilometraje personalizado         2.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{31}: Freno personalizado               2.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{32}: Modificar todos los autos         5.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{33}: Modificar Shiftime                2.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{34}: Modificar Dezlizamiento llantas   2.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{35}: Modificar Recorrido llantas       2.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{36}: Modificar Rigidez llantas         2.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{37}: Modificar Inclinacion llantas     2.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{38}: Modificar Visibilidad  vidrios    2.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{39}: Cambiar Contraseña                2.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{40}: Cambiar correo electrónico        2.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{41}: Quitar parachoques trasero        2.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{42}: Quitar parachoques delantero      2.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{43}: Copiar diseño de un auto a otro   2.000'))
    print(Colorate.Horizontal(Colors.rainbow, '{44}: Clonar Placas                     2.500'))
    print(Colorate.Horizontal(Colors.rainbow, '{45}: Calipers y luces cromo            2.500'))
    print(Colorate.Horizontal(Colors.rainbow, '{46}: Cromar Auto Completo              3.500'))
    print(Colorate.Horizontal(Colors.rainbow, '{0} : Salir'))
    
    print(Colorate.Horizontal(Colors.rainbow, '===============[ 𝐋𝐄𝐔𝐍𝐀𝐌 ]==============='))

def procesar_servicio(service, cpm, console):
    """Procesa el servicio seleccionado por el usuario"""
    try:
        if service == 0:  # Salir
            print(Colorate.Horizontal(Colors.rainbow, f'Gracias por usar nuestra herramienta, únete a nuestro canal de telegram: @{__CHANNEL_USERNAME__}.'))
            sys.exit(0)
        elif service == 1: # Aumentar dinero
            print(Colorate.Horizontal(Colors.rainbow, '[?] Ingresa cuánto dinero deseas.'))
            amount = IntPrompt.ask("[?] Cantidad")
            console.print("[%] Guardando tus datos: ", end=None)
            if amount > 0 and amount <= 500000000000000000000000000000000:
                if cpm.set_player_money(amount):
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Por favor inténtalo de nuevo.'))
                    sleep(2)
                    return False
            else:
                print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                print(Colorate.Horizontal(Colors.rainbow, 'Por favor usa valores válidos.'))
                sleep(2)
                return False
        elif service == 2: # Aumentar monedas
            print(Colorate.Horizontal(Colors.rainbow, '[?] Ingresa cuántas monedas deseas.'))
            amount = IntPrompt.ask("[?] Cantidad")
            console.print("[%] Guardando tus datos: ", end=None)
            if amount > 0 and amount <= 500000000000000:
                if cpm.set_player_coins(amount):
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Por favor inténtalo de nuevo.'))
                    sleep(2)
                    return False
            else:
                print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                print(Colorate.Horizontal(Colors.rainbow, 'Por favor usa valores válidos.'))
                sleep(2)
                return False
        elif service == 3: # Rango Rey
            console.print("[bold red][!] Nota:[/bold red] si el rango de rey no aparece en el juego, ciérralo y ábrelo varias veces.")
            console.print("[bold red][!] Nota:[/bold red] por favor no hagas Rango Rey en la misma cuenta dos veces.")
            sleep(2)
            console.print("[%] Dándote el Rango Rey: ", end=None)
            if cpm.set_player_rank():
                print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                check_exit()
            else:
                print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                print(Colorate.Horizontal(Colors.rainbow, 'Por favor inténtalo de nuevo.'))
                sleep(2)
                return False
        elif service == 4: # Cambiar ID
            print(Colorate.Horizontal(Colors.rainbow, '[?] Ingresa tu nuevo ID.'))
            new_id = Prompt.ask("[?] ID")
            console.print("[%] Guardando tus datos: ", end=None)
            if len(new_id) >= 0 and len(new_id) <= 9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999 and (' ' in new_id) == False:
                if cpm.set_player_localid(new_id.upper()):
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Por favor inténtalo de nuevo.'))
                    sleep(2)
                    return False
            else:
                print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                print(Colorate.Horizontal(Colors.rainbow, 'Por favor usa valores válidos.'))
                sleep(2)
                return False
  
