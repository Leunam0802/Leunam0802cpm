from pystyle import Box
import random
import requests
from time import sleep
import os, signal, sys
from pyfiglet import figlet_format
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich.style import Style
import json
import pystyle
from pystyle import Colors, Colorate

from leunamcpm import leunamcpm

__CHANNEL_USERNAME__ = "Leunam0802"
__GROUP_USERNAME__   = "https://t.me/+JDaiBsc8CQUxODQ5"

def check_exit():
    answ = Prompt.ask("[?] ¿Quieres salir?", choices=["y", "n"], default="n")
    if answ == "y":
        print(Colorate.Horizontal(Colors.rainbow, f'Gracias por usar nuestra herramienta, únete a nuestro canal de telegram: @{__CHANNEL_USERNAME__}.'))
        sys.exit(0)

def signal_handler(sig, frame):
    print("\n Adiós...")
    sys.exit(0)

def gradient_text(text, colors):
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
    os.system('cls' if os.name == 'nt' else 'clear')
    # Tu nombre aquí
    brand_name = figlet_format('Leunam', font='starwars')  
    colors = [
        "rgb(255,0,0)", "rgb(255,69,0)", "rgb(255,140,0)", "rgb(255,215,0)", "rgb(173,255,47)", 
    ]
    colorful_text = gradient_text(brand_name, colors)
    console.print(colorful_text)
    print(Colorate.Horizontal(Colors.rainbow, '============================================================'))
    print(Colorate.Horizontal(Colors.rainbow, '\t         POR FAVOR CIERRA SESIÓN EN CPM ANTES DE USAR ESTA HERRAMIENTA'))
    print(Colorate.Horizontal(Colors.rainbow, '    COMPARTIR LA CLAVE DE ACCESO NO ESTÁ PERMITIDO Y SERÁ BLOQUEADO'))
    print(Colorate.Horizontal(Colors.rainbow, f' ‌           Telegram: @{__CHANNEL_USERNAME__} O {__GROUP_USERNAME__}'))
    print(Colorate.Horizontal(Colors.rainbow, '=======================================================

def load_player_data(cpm):
    response = cpm.get_player_data()
    if response.get('ok'):
        data = response.get('data')
        if 'floats' in data and 'localID' in data and 'money' in data and 'coin' in data:
        
            print(Colorate.Horizontal(Colors.rainbow, '==========[ DETALLES DEL JUGADOR ]=========='))
            
            print(Colorate.Horizontal(Colors.rainbow, f'Nombre   : {(data.get("Name") if "Name" in data else "INDEFINIDO")}.'))
                
            print(Colorate.Horizontal(Colors.rainbow, f'LocalID: {data.get("localID")}.'))
            
            print(Colorate.Horizontal(Colors.rainbow, f'Dinero  : {data.get("money")}.'))
            
            print(Colorate.Horizontal(Colors.rainbow, f'Monedas  : {data.get("coin")}.'))
            
        else:
            print(Colorate.Horizontal(Colors.rainbow, '! ERROR: las cuentas nuevas deben iniciar sesión en el juego al menos una vez !.'))
            exit(1)
    else:
        print(Colorate.Horizontal(Colors.rainbow, '! ERROR: parece que tu inicio de sesión no está configurado correctamente !.'))
        exit(1)


def load_key_data(cpm):

    data = cpm.get_key_data()
    
    print(Colorate.Horizontal(Colors.rainbow, '========[ DETALLES DE CLAVE DE ACCESO ]========'))
    
    print(Colorate.Horizontal(Colors.rainbow, f'Clave de acceso : {data.get("access_key")}.'))
    
    print(Colorate.Horizontal(Colors.rainbow, f'ID de Telegram: {data.get("telegram_id")}.'))
    
    print(Colorate.Horizontal(Colors.rainbow, f'Saldo $  : {(data.get("coins") if not data.get("is_unlimited") else "Ilimitado")}.'))
        
    

def prompt_valid_value(content, tag, password=False):
    while True:
        value = Prompt.ask(content, password=password)
        if not value or value.isspace():
            print(Colorate.Horizontal(Colors.rainbow, f'{tag} no puede estar vacío o solo espacios. Por favor intente nuevamente.'))
        else:
            return value
            
def load_client_details():
    response = requests.get("http://ip-api.com/json")
    data = response.json()
    print(Colorate.Horizontal(Colors.rainbow, '=============[ UBICACIÓN ]============='))
    print(Colorate.Horizontal(Colors.rainbow, f'Dirección IP : {data.get("query")}.'))
    print(Colorate.Horizontal(Colors.rainbow, f'Ubicación   : {data.get("city")} {data.get("regionName")} {data.get("countryCode")}.'))
    print(Colorate.Horizontal(Colors.rainbow, f'País    : {data.get("country")} {data.get("zip")}.'))
    print(Colorate.Horizontal(Colors.rainbow, '===============[ MENÚ ]==============='))

def interpolate_color(start_color, end_color, fraction):
    start_rgb = tuple(int(start_color[i:i+2], 16) for i in (1, 3, 5))
    end_rgb = tuple(int(end_color[i:i+2], 16) for i in (1, 3, 5))
    interpolated_rgb = tuple(int(start + fraction * (end - start)) for start, end in zip(start_rgb, end_rgb))
    return "{:02x}{:02x}{:02x}".format(*interpolated_rgb)

def rainbow_gradient_string(customer_name):
    modified_string = ""
    num_chars = len(customer_name)
    start_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    end_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    for i, char in enumerate(customer_name):
        fraction = i / max(num_chars - 1, 1)
        interpolated_color = interpolate_color(start_color, end_color, fraction)
        modified_string += f'[{interpolated_color}]{char}'
    return modified_string

def modificar_todos_los_autos(cpm, hp, hp_interno, nm, torque):
    try:
        response = cpm.modificar_todos_los_autos(hp, hp_interno, nm, torque)
        if response:
            print(Colorate.Horizontal(Colors.rainbow, 'Todos los autos han sido modificados exitosamente.'))
        else:
            print(Colorate.Horizontal(Colors.rainbow, 'Error al modificar los autos.'))
    except Exception as e:
        print(Colorate.Horizontal(Colors.rainbow, f'Error: {e}'))

if __name__ == "__main__":
    console = Console()
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        banner(console)
        acc_email = prompt_valid_value("[bold][?] Correo electrónico de la cuenta[/bold]", "Correo electrónico", password=False)
        acc_password = prompt_valid_value("[bold][?] Contraseña de la cuenta[/bold]", "Contraseña", password=False)
        acc_access_key = prompt_valid_value("[bold][?] Clave de acceso[/bold]", "Clave de acceso", password=False)
        console.print("[bold cyan][%] Intentando iniciar sesión[/bold cyan]: ", end=None)
        cpm = tornercpm1(acc_access_key)
        login_response = cpm.login(acc_email, acc_password)
        if login_response != 0:
            if login_response == 100:
                print(Colorate.Horizontal(Colors.rainbow, 'CUENTA NO ENCONTRADA.'))
                sleep(2)
                continue
            elif login_response == 101:
                print(Colorate.Horizontal(Colors.rainbow, 'CONTRASEÑA INCORRECTA.'))
                sleep(2)
                continue
            elif login_response == 103:
                print(Colorate.Horizontal(Colors.rainbow, 'CLAVE DE ACCESO INVÁLIDA.'))
                sleep(2)
                continue
            else:
                print(Colorate.Horizontal(Colors.rainbow, 'INTENTAR DE NUEVO.'))
                print(Colorate.Horizontal(Colors.rainbow, '! Nota: asegúrate de completar todos los campos !.'))
                sleep(2)
                continue
        else:
            print(Colorate.Horizontal(Colors.rainbow, 'ÉXITO.'))
            sleep(2)
        while True:
            banner(console)
            load_player_data(cpm)
            load_key_data(cpm)
            load_client_details()
            choices = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46"]
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
            
            print(Colorate.Horizontal(Colors.rainbow, '===============[ 𝐓𝐎𝐑𝐍𝐄𝐑 ]==============='))
            
            service = IntPrompt.ask(f"[bold][?] Selecciona un servicio [red][1-{choices[-1]} o 0][/red][/bold]", choices=choices, show_choices=False)
            
            print(Colorate.Horizontal(Colors.rainbow, '===============[ 𝐓𝐎𝐑𝐍𝐄𝐑 ]==============='))
            
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
            