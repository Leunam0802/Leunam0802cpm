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
            
    service = IntPrompt.ask(f"[bold][?] Selecciona un servicio [red][1-{choices[-1]} o 0][/red][/bold]", choices=choices, show_choices=False)
            
    print(Colorate.Horizontal(Colors.rainbow, '===============[ 𝐋𝐄𝐔𝐍𝐀𝐌 ]==============='))
            
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
                        continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Por favor usa valores válidos.'))
                    sleep(2)
                    continue
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
                        continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Por favor usa valores válidos.'))
                    sleep(2)
                    continue
            elif service == 3: # Rango Rey
                console.print("[bold red][!] Nota:[/bold red]: si el rango de rey no aparece en el juego, ciérralo y ábrelo varias veces.", end=None)
                console.print("[bold red][!] Nota:[/bold red]: por favor no hagas Rango Rey en la misma cuenta dos veces.", end=None)
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
                    continue
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
                        continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Por favor usa un ID válido.'))
                    sleep(2)
                    continue
            elif service == 5: # Cambiar Nombre
                print(Colorate.Horizontal(Colors.rainbow, '[?] Ingresa tu nuevo nombre.'))
                new_name = Prompt.ask("[?] Nombre")
                console.print("[%] Guardando tus datos: ", end=None)
                if len(new_name) >= 0 and len(new_name) <= 999999999:
                    if cpm.set_player_name(new_name):
                        print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                        print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                        check_exit()
                    else:
                        print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                        print(Colorate.Horizontal(Colors.rainbow, 'Por favor inténtalo de nuevo.'))
                        sleep(2)
                        continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Por favor usa valores válidos.'))
                    sleep(2)
                    continue
            elif service == 6: # Cambiar Nombre Arcoíris
                print(Colorate.Horizontal(Colors.rainbow, '[?] Ingresa tu nuevo nombre arcoíris.'))
                new_name = Prompt.ask("[?] Nombre")
                console.print("[%] Guardando tus datos: ", end=None)
                if len(new_name) >= 0 and len(new_name) <= 999999999:
                    if cpm.set_player_name(rainbow_gradient_string(new_name)):
                        print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                        print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                        check_exit()
                    else:
                        print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                        print(Colorate.Horizontal(Colors.rainbow, 'Por favor inténtalo de nuevo.'))
                        sleep(2)
                        continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Por favor usa valores válidos.'))
                    sleep(2)
                    continue
            elif service == 7: # Placas de número
                console.print("[%] Dándote placas de número: ", end=None)
                if cpm.set_player_plates():
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Por favor inténtalo de nuevo.'))
                    sleep(2)
                    continue
            elif service == 8: # Eliminar cuenta
                print(Colorate.Horizontal(Colors.rainbow, '[!] Después de eliminar tu cuenta no hay vuelta atrás !!.'))
                answ = Prompt.ask("[?] ¿Quieres eliminar esta cuenta?!", choices=["y", "n"], default="n")
                if answ == "y":
                    cpm.delete()
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    print(Colorate.Horizontal(Colors.rainbow, f'Gracias por usar nuestra herramienta, únete a nuestro canal de telegram: @{__CHANNEL_USERNAME__}.'))
                else: continue
            elif service == 9: # Registrar cuenta
                print(Colorate.Horizontal(Colors.rainbow, '[!] Registrando nueva cuenta.'))
                acc2_email = prompt_valid_value("[?] Correo electrónico de la cuenta", "Correo electrónico", password=False)
                acc2_password = prompt_valid_value("[?] Contraseña de la cuenta", "Contraseña", password=False)
                console.print("[%] Creando nueva cuenta: ", end=None)
                status = cpm.register(acc2_email, acc2_password)
                if status == 0:
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    print(Colorate.Horizontal(Colors.rainbow, f'INFO: Para modificar esta cuenta con CPMElsedev.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'debes iniciar sesión en el juego con esta cuenta.'))
                    sleep(2)
                    continue
                elif status == 105:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, '¡Este correo electrónico ya existe!.'))
                    sleep(2)
                    continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Por favor inténtalo de nuevo.'))
                    sleep(2)
                    continue
            elif service == 10: # Eliminar amigos
                console.print("[%] Eliminando tus amigos: ", end=None)
                if cpm.delete_player_friends():
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Por favor inténtalo de nuevo.'))
                    sleep(2)
                    continue
            elif service == 11: # Desbloquear autos pagados
                console.print("[!] Nota: esta función tarda un tiempo en completarse, por favor no canceles.", end=None)
                console.print("[%] Desbloqueando autos pagados: ", end=None)
                if cpm.unlock_paid_cars():
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Por favor inténtalo de nuevo.'))
                    sleep(2)
                    continue
            elif service == 12: # Desbloquear todos los autos
                console.print("[%] Desbloqueando todos los autos: ", end=None)
                if cpm.unlock_all_cars():
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Por favor inténtalo de nuevo.'))
                    sleep(2)
                    continue
            elif service == 13: # Desbloquear sirenas de autos
                console.print("[%] Desbloqueando sirenas de autos: ", end=None)
                if cpm.unlock_all_cars_siren():
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Por favor inténtalo de nuevo.'))
                    sleep(2)
                    continue
            elif service == 14: # Desbloquear motor w16
                console.print("[%] Desbloqueando motor w16: ", end=None)
                if cpm.unlock_w16():
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Por favor inténtalo de nuevo.'))
                    sleep(2)
                    continue
            elif service == 15: # Desbloquear todas las bocinas
                console.print("[%] Desbloqueando todas las bocinas: ", end=None)
                if cpm.unlock_horns():
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Por favor inténtalo de nuevo.'))
                    sleep(2)
                    continue
            elif service == 16: # Desactivar daños del motor
                console.print("[%] Desbloqueando sin daños: ", end=None)
                if cpm.disable_engine_damage():
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Por favor inténtalo de nuevo.'))
                    sleep(2)
                    continue
            elif service == 17: # Combustible ilimitado
                console.print("[%] Desbloqueando combustible ilimitado: ", end=None)
                if cpm.unlimited_fuel():
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Por favor inténtalo de nuevo.'))
                    sleep(2)
                    continue
            elif service == 18: # Desbloquear Casa 3
                console.print("[%] Desbloqueando Casa 3: ", end=None)
                if cpm.unlock_houses():
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Por favor inténtalo de nuevo.'))
                    sleep(2)
                    continue
            elif service == 19: # Desbloquear humo
                console.print("[%] Desbloqueando humo: ", end=None)
                if cpm.unlock_smoke():
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Por favor inténtalo de nuevo.'))
                    sleep(2)
                    continue
            elif service == 20: # Desbloquear llantas
                console.print("[%] Desbloqueando llantas: ", end=None)
                if cpm.unlock_wheels():
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Por favor inténtalo de nuevo.'))
                    sleep(2)
                    continue
            elif service == 21: # Desbloquear animaciones
                console.print("[%] Desbloqueando animaciones: ", end=None)
                if cpm.unlock_animations():
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Por favor inténtalo de nuevo.'))
                    sleep(2)
                    continue
            elif service == 22: # Desbloquear equipos masculinos
                console.print("[%] Desbloqueando equipos masculinos: ", end=None)
                if cpm.unlock_equipments_male():
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Por favor inténtalo de nuevo.'))
                    sleep(2)
                    continue
            elif service == 23: # Desbloquear equipos femeninos
                console.print("[%] Desbloqueando equipos femeninos: ", end=None)
                if cpm.unlock_equipments_female():
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Por favor inténtalo de nuevo.'))
                    sleep(2)
                    continue
            elif service == 24: # Cambiar carreras ganadas
                print(Colorate.Horizontal(Colors.rainbow, '[!] Ingresa cuántas carreras has ganado.'))
                amount = IntPrompt.ask("[?] Cantidad")
                console.print("[%] Cambiando tus datos: ", end=None)
                if amount > 0 and amount <= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
                    if cpm.set_player_wins(amount):
                        print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                        print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                        check_exit()
                    else:
                        print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                        print(Colorate.Horizontal(Colors.rainbow, '[!] Por favor usa valores válidos.'))
                        sleep(2)
                        continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, '[!] Por favor usa valores válidos.'))
                    sleep(2)
                    continue
            elif service == 25: # Cambiar carreras perdidas
                print(Colorate.Horizontal(Colors.rainbow, '[!] Ingresa cuántas carreras has perdido.'))
                amount = IntPrompt.ask("[?] Cantidad")
                console.print("[%] Cambiando tus datos: ", end=None)
                if amount > 0 and amount <= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
                    if cpm.set_player_loses(amount):
                        print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                        print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                        check_exit()
                    else:
                        print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                        print(Colorate.Horizontal(Colors.rainbow, '[!] Por favor usa valores válidos.'))
                        sleep(2)
                        continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, '[!] Por favor usa valores válidos.'))
                    sleep(2)
                    continue
            elif service == 26: # Clonar cuenta
                print(Colorate.Horizontal(Colors.rainbow, '[!] Por favor ingresa los detalles de la cuenta.'))
                to_email = prompt_valid_value("[?] Correo electrónico de la cuenta", "Correo electrónico", password=False)
                to_password = prompt_valid_value("[?] Contraseña de la cuenta", "Contraseña", password=False)
                console.print("[%] Clonando tu cuenta: ", end=None)
                if cpm.account_clone(to_email, to_password):
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    check_exit()
                else:     
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, '[!] LA CUENTA RECEPTORA ES GMAIL, LA CONTRASEÑA NO ES VÁLIDA O ESA CUENTA NO ESTÁ REGISTRADA.'))
                    sleep(2)
                    continue
            elif service == 27: # HP personalizado
                console.print("[bold yellow][!] Nota[/bold yellow]: ¡la velocidad original no se puede restaurar!.")
                console.print("[bold cyan][!] Ingresa los detalles del auto.[/bold cyan]")
                car_id = IntPrompt.ask("[bold][?] ID del auto[/bold]")
                new_hp = IntPrompt.ask("[bold][?] Ingresa nuevo HP[/bold]")
                new_inner_hp = IntPrompt.ask("[bold][?] Ingresa nuevo HP interno[/bold]")
                new_nm = IntPrompt.ask("[bold][?] Ingresa nuevo NM[/bold]")
                new_torque = IntPrompt.ask("[bold][?] Ingresa nuevo torque[/bold]")
                console.print("[bold cyan][%] Hackeando velocidad del auto[/bold cyan]:", end=None)
                if cpm.hack_car_speed(car_id, new_hp, new_inner_hp, new_nm, new_torque):
                    console.print("[bold green]ÉXITO (✔)[/bold green]")
                    console.print("================================")
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, '[!] Por favor usa valores válidos.'))
                    sleep(2)
                    continue
            elif service == 28: # Ángulo personalizado
                print(Colorate.Horizontal(Colors.rainbow, '[!] INGRESA DETALLES DEL AUTO'))
                car_id = IntPrompt.ask("[bold][?] ID DEL AUTO[/bold]")
                print(Colorate.Horizontal(Colors.rainbow, '[!] INGRESA ÁNGULO DE DIRECCIÓN'))
                custom = IntPrompt.ask("[red][?]﻿INGRESA LA CANTIDAD DE ÁNGULO QUE DESEAS[/red]")                
                console.print("[red][%] HACKEANDO ÁNGULO DEL AUTO[/red]: ", end=None)
                if cpm.max_max1(car_id, custom):
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ'))
                    print(Colorate.Horizontal(Colors.rainbow, 'POR FAVOR INTENTA DE NUEVO'))
                    sleep(2)
                    continue
            elif service == 29: # Quemado de llantas personalizado
                print(Colorate.Horizontal(Colors.rainbow, '[!] INGRESA DETALLES DEL AUTO'))
                car_id = IntPrompt.ask("[bold][?] ID DEL AUTO[/bold]")
                print(Colorate.Horizontal(Colors.rainbow, '[!] INGRESA PORCENTAJE'))
                custom = IntPrompt.ask("[pink][?]﻿INGRESA PORCENTAJE DE LLANTAS QUE DESEAS[/pink]")                
                console.print("[red][%] Configurando porcentaje [/red]: ", end=None)
                if cpm.max_max2(car_id, custom):
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ'))
                    print(Colorate.Horizontal(Colors.rainbow, 'POR FAVOR INTENTA DE NUEVO'))
                    sleep(2)
                    continue
            elif service == 30: # Kilometraje personalizado
                console.print("[bold]INGRESA DETALLES DEL AUTO![/bold]")
                car_id = IntPrompt.ask("[bold][?] ID DEL AUTO[/bold]")
                console.print("[bold]INGRESA NUEVO KILOMETRAJE![/bold]")
                custom = IntPrompt.ask("[bold blue][?]﻿INGRESA KILOMETRAJE QUE DESEAS[/bold blue]")                
                console.print("[bold red][%] Configurando porcentaje [/bold red]: ", end=None)
                if cpm.millage_car(car_id, custom):
                    console.print("[bold green]ÉXITO (✔)[/bold green]")
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ'))
                    print(Colorate.Horizontal(Colors.rainbow, 'POR FAVOR INTENTA DE NUEVO'))
                    sleep(2)
                    continue
            elif service == 31: # Freno personalizado
                console.print("[bold]INGRESA DETALLES DEL AUTO![/bold]")
                car_id = IntPrompt.ask("[bold][?] ID DEL AUTO[/bold]")
                console.print("[bold]INGRESA NUEVO FRENO![/bold]")
                custom = IntPrompt.ask("[bold blue][?]﻿INGRESA FRENO QUE DESEAS[/bold blue]")                
                console.print("[bold red][%] Configurando FRENO [/bold red]: ", end=None)
                if cpm.brake_car(car_id, custom):
                    console.print("[bold green]ÉXITO (✔)[/bold green]")
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ'))
                    print(Colorate.Horizontal(Colors.rainbow, 'POR FAVOR INTENTA DE NUEVO'))
                    sleep(2)
                    continue
            elif service == 32: # Modificar todos los autos
                console.print("[bold]INGRESA DETALLES PARA MODIFICAR TODOS LOS AUTOS![/bold]")
                new_hp = IntPrompt.ask("[bold][?] Ingresa nuevo HP[/bold]")
                new_inner_hp = IntPrompt.ask("[bold][?] Ingresa nuevo HP interno[/bold]")
                new_nm = IntPrompt.ask("[bold][?] Ingresa nuevo NM[/bold]")
                new_torque = IntPrompt.ask("[bold][?] Ingresa nuevo torque[/bold]")
                console.print("[bold red][%] Modificando todos los autos [/bold red]: ", end=None)
                modificar_todos_los_autos(cpm, new_hp, new_inner_hp, new_nm, new_torque)
                check_exit()
            elif service == 33: # Shiftime
                print(Colorate.Horizontal(Colors.rainbow, '[!] INGRESA DETALLES DEL AUTO'))
                car_id = IntPrompt.ask("[bold][?] ID DEL AUTO[/bold]")
                print(Colorate.Horizontal(Colors.rainbow, '[!] INGRESA VALORES SHIFTIME'))
                custom_input = Prompt.ask("[red][?] INGRESA LOS VALORES DE TU SHIFTIME[/red]")
                try:
                    custom = float(custom_input)
                except ValueError:
                    print(Colorate.Horizontal(Colors.rainbow, 'VALOR INVÁLIDO, POR FAVOR INGRESA UN NÚMERO'))
                    sleep(2)
                    continue
                
                console.print("[red][%] HACKEANDO SHIFTIME DEL AUTO[/red]: ", end=None)
                if cpm.Shiftime(car_id, custom):
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ'))
                    print(Colorate.Horizontal(Colors.rainbow, 'POR FAVOR INTENTA DE NUEVO'))
                    sleep(2)
                    continue
            elif service == 34: # Cambiar dezlizamiento
                print(Colorate.Horizontal(Colors.rainbow, '[!] INGRESA DETALLES DEL AUTO'))
                car_id = IntPrompt.ask("[bold][?] ID DEL AUTO[/bold]")
                print(Colorate.Horizontal(Colors.rainbow, '[!] INGRESA PORCENTAJE'))
                custom = IntPrompt.ask("[pink][?]﻿INGRESA PORCENTAJE DE DEZLIZAMIENTO[/pink]")                
                console.print("[red][%] Configurando porcentaje [/red]: ", end=None)
                if cpm.Dez(car_id, custom):
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ'))
                    print(Colorate.Horizontal(Colors.rainbow, 'POR FAVOR INTENTA DE NUEVO'))
                    sleep(2)
                    continue
            elif service == 35: # Cambiar Recorrido
                print(Colorate.Horizontal(Colors.rainbow, '[!] INGRESA DETALLES DEL AUTO'))
                car_id = IntPrompt.ask("[bold][?] ID DEL AUTO[/bold]")
                print(Colorate.Horizontal(Colors.rainbow, '[!] INGRESA PORCENTAJE'))
                custom = IntPrompt.ask("[pink][?]﻿INGRESA PORCENTAJE DE RECORRIDO[/pink]")                
                console.print("[red][%] Configurando porcentaje [/red]: ", end=None)
                if cpm.Rec(car_id, custom):
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ'))
                    print(Colorate.Horizontal(Colors.rainbow, 'POR FAVOR INTENTA DE NUEVO'))
                    sleep(2)
                    continue  
            elif service == 36: # Cambiar 
                print(Colorate.Horizontal(Colors.rainbow, '[!] INGRESA DETALLES DEL AUTO'))
                car_id = IntPrompt.ask("[bold][?] ID DEL AUTO[/bold]")
                print(Colorate.Horizontal(Colors.rainbow, '[!] INGRESA PORCENTAJE'))
                custom = IntPrompt.ask("[pink][?]﻿INGRESA PORCENTAJE DE RIGIDEZ[/pink]")                
                console.print("[red][%] Configurando porcentaje [/red]: ", end=None)
                if cpm.Rig(car_id, custom):
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ'))
                    print(Colorate.Horizontal(Colors.rainbow, 'POR FAVOR INTENTA DE NUEVO'))
                    sleep(2)
                    continue   
            elif service == 37: # Cambiar inclinacion
                print(Colorate.Horizontal(Colors.rainbow, '[!] INGRESA DETALLES DEL AUTO'))
                car_id = IntPrompt.ask("[bold][?] ID DEL AUTO[/bold]")
                print(Colorate.Horizontal(Colors.rainbow, '[!] INGRESA PORCENTAJE'))
                
                while True:
                    try:
                        custom_input = Prompt.ask("[pink][?] INGRESA PORCENTAJE DE INCLINACION[/pink]")
                        # Reemplazar comas por puntos para uniformidad
                        custom_input = custom_input.replace(',', '.')
                        # Convertir a float
                        custom = float(custom_input)
                        break
                    except ValueError:
                        print(Colorate.Horizontal(Colors.red, '[!] PORCENTAJE INVÁLIDO. USA NÚMEROS CON PUNTO O COMA DECIMAL'))
                        continue
                
                console.print("[red][%] Configurando porcentaje [/red]: ", end=None)
                if cpm.Inc(car_id, custom):
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ'))
                    print(Colorate.Horizontal(Colors.rainbow, 'POR FAVOR INTENTA DE NUEVO'))
                    sleep(2)
                    continue 
            elif service == 38: # Cambiar VISI DE VIDRIOS
                print(Colorate.Horizontal(Colors.rainbow, '[!] INGRESA DETALLES DEL AUTO'))
                car_id = IntPrompt.ask("[bold][?] ID DEL AUTO[/bold]")
                print(Colorate.Horizontal(Colors.rainbow, '[!] INGRESA PORCENTAJE'))
                custom = IntPrompt.ask("[pink][?]﻿INGRESA PORCENTAJE DE VISIB DE LOS VIDRIOS[/pink]")                
                console.print("[red][%] Configurando porcentaje [/red]: ", end=None)
                if cpm.Vid(car_id, custom):
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ'))
                    print(Colorate.Horizontal(Colors.rainbow, 'POR FAVOR INTENTA DE NUEVO'))
                    sleep(2)
                    continue                                                                                         
            elif service == 39: # Cambiar contraseña
                print(Colorate.Horizontal(Colors.rainbow, '[!] Por favor ingresa la nueva contraseña'))
                new_password = prompt_valid_value("[?] Nueva contraseña", "Contraseña", password=True)
                
                console.print("[%] Cambiando contraseña: ", end=None)
                if cpm.change_password(new_password):
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    check_exit()
                else:     
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, '[!] La contraseña debe tener al menos 6 caracteres o hubo un error en la conexión.'))
                    sleep(2)
                    continue
            elif service == 40: # Cambiar correo electrónico
                print(Colorate.Horizontal(Colors.rainbow, '[!] Por favor ingresa el nuevo correo electrónico'))
                new_email = prompt_valid_value("[?] Nuevo correo electrónico", "Correo electrónico", password=False)
                
                console.print("[%] Cambiando correo electrónico: ", end=None)
                if cpm.change_email(new_email):
                    print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    check_exit()
                else:     
                    print(Colorate.Horizontal(Colors.rainbow, 'FALLÓ.'))
                    print(Colorate.Horizontal(Colors.rainbow, '[!] El correo electrónico no es válido, ya está en uso o hubo un error en la conexión.'))
                    sleep(2)
                    continue     
            elif service == 41: # Bumper rear
                console.print("[bold]Escribe los detalles de tu auto![/bold]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")                
                console.print("[bold red][%] Removiendo Bumper Trasero [/bold red]: ", end=None)
                if cpm.rear_bumper(car_id):
                    console.print("[bold green]Exito (✔️)[/bold green]")
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'Fallo'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Intenta de nuevo'))
                    sleep(2)
                    continue
            elif service == 42:  # Bumper front
                console.print("[bold]Escribe los detalles de tu auto![/bold]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")                
                console.print("[bold red][%] Removiendo Bumper Frontal [/bold red]: ", end=None)
                if cpm.front_bumper(car_id):
                    console.print("[bold green]Exito (✔️)[/bold green]")
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'Fallo'))
                    print(Colorate.Horizontal(Colors.rainbow, 'Intenta de nuevo'))
                    sleep(2)
                    continue       
            elif service == 43:  # Copiar diseño de un auto a otro
                console.print("[bold]Copiando diseño de un auto a otro...[/bold]")
                source_id = IntPrompt.ask("[bold cyan][?] Ingresa el ID del auto origen[/bold cyan]")
                target_id = IntPrompt.ask("[bold cyan][?] Ingresa el ID del auto destino[/bold cyan]")
                console.print("[bold red][%] Aplicando diseño del auto origen al destino...[/bold red]", end=None)
                if cpm.clone_car_design(source_id, target_id):
                    print(Colorate.Horizontal(Colors.rainbow, f"✔ El diseño del auto {source_id} fue copiado al auto {target_id} exitosamente."))
                    check_exit()
                else:
                    print(Colorate.Horizontal(Colors.red_to_white, f"❌ No se pudo copiar el diseño del auto {source_id}."))
                    sleep(2)
                    continue
            elif service == 44:  # Clonar solo placas entre cuentas
                console.print("[bold cyan]Clonador de placas activado[/bold cyan]")
                to_email = Prompt.ask("[bold][?] Correo de destino[/bold]")
                to_password = Prompt.ask("[bold][?] Contraseña de destino[/bold]", password=True)

                console.print("[bold red][%] Clonando placas...[/bold red]")
                resultado = cpm.clone_plates_only(to_email, to_password)

                if resultado:
                    print(Colorate.Horizontal(Colors.rainbow, "✔ Placas clonadas exitosamente"))
                else:
                    print(Colorate.Horizontal(Colors.red_to_white, "❌ Error al clonar placas"))

                check_exit()
            elif service == 45:  # Aplicar luces/calipers cromados
                console.print("[bold cyan]Clonador de luces y calipers cromados activado[/bold cyan]")
                car_id = IntPrompt.ask("[bold][?] Ingresa el ID del auto donde aplicar[/bold]")
                color = IntPrompt.ask("[bold][?] Ingresa el número de color[/bold]\n[1=Rojo, 2=Verde, 3=Azul, 4=Celeste, 5=Naranja, 6=Rosa, 7=Purpura, 8=Blanco]")

                console.print("[bold red][%] Aplicando componentes...[/bold red]")
                resultado = cpm.apply_chrome_parts(car_id, color)

                if resultado.get("ok"):
                    print(Colorate.Horizontal(Colors.rainbow, "✔ Componentes aplicados correctamente"))
                else:
                    print(Colorate.Horizontal(Colors.red_to_white, f"❌ Error: {resultado.get('message')}"))

                check_exit()
            elif service == 46:  # Aplicar pintura del coche y ventanas
                console.print("[bold cyan]Clonador de pintura activado[/bold cyan]")
                car_id = IntPrompt.ask("[bold][?] Ingresa el ID del auto donde aplicar[/bold]")

                console.print("[bold red][%] Aplicando pintura...[/bold red]")
                resultado = cpm.apply_paint_only(car_id)

                if resultado.get("ok"):
                    print(Colorate.Horizontal(Colors.rainbow, "✔ Pintura aplicada correctamente"))
                else:
                    print(Colorate.Horizontal(Colors.red_to_white, f"❌ Error: {resultado.get('message')}"))

                check_exit()