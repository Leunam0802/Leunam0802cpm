#!/usr/bin/env python
import logging
import os
import requests
import json

# Configuración del logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

class leunamcpm:
    """
    Clase para manejar las operaciones de CPM
    """
    
    def __init__(self, access_key):
        """Inicializa la clase con la clave de acceso"""
        self.access_key = access_key
        self.session = requests.Session()
        self.base_url = "https://api.leunam0802.com/cpm"
        self.player_data = None
        self.logged_in = False
        self.email = None
        self.password = None
        
        # Añadir cabeceras comunes para todas las solicitudes
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "CPM-Client/1.0",
            "X-Access-Key": self.access_key
        })
    
    def login(self, email, password):
        """
        Intenta iniciar sesión con el email y contraseña proporcionados
        Retorna:
        0 = Éxito
        100 = Cuenta no encontrada
        101 = Contraseña incorrecta
        103 = Clave de acceso inválida
        """
        self.email = email
        self.password = password
        
        try:
            # Preparamos los datos para la solicitud
            login_data = {
                "email": email,
                "password": password,
                "access_key": self.access_key
            }
            
            # Hacemos la petición a la API real
            response = self.session.post(f"{self.base_url}/login", json=login_data)
            
            # Analizamos la respuesta
            if response.status_code == 200:
                response_data = response.json()
                if response_data.get("ok", False):
                    self.logged_in = True
                    self._load_player_data()
                    logger.info(f"Inicio de sesión exitoso para: {email}")
                    return 0
                else:
                    error_code = response_data.get("error_code", -1)
                    logger.warning(f"Error al iniciar sesión: {response_data.get('message')} (código: {error_code})")
                    return error_code
            else:
                logger.error(f"Error HTTP {response.status_code} al iniciar sesión")
                return -1
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error de conexión en login: {e}")
            return -2
        except json.JSONDecodeError as e:
            logger.error(f"Error al decodificar respuesta JSON: {e}")
            return -3
        except Exception as e:
            logger.error(f"Error inesperado en login: {e}")
            return -1
    
    def _load_player_data(self):
        """Método interno para cargar los datos del jugador"""
        try:
            # Hacemos la petición para obtener los datos del jugador
            response = self.session.get(f"{self.base_url}/player_data")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("ok", False):
                    self.player_data = data.get("data", {})
                    logger.info("Datos del jugador cargados correctamente")
                else:
                    logger.warning(f"No se pudieron cargar los datos del jugador: {data.get('message')}")
            else:
                logger.error(f"Error HTTP {response.status_code} al cargar datos del jugador")
        except Exception as e:
            logger.error(f"Error al cargar datos del jugador: {e}")
    
    def get_player_data(self):
        """Obtiene los datos del jugador"""
        if not self.logged_in:
            return {"ok": False, "message": "No has iniciado sesión"}
        
        try:
            # Refrescamos los datos del jugador
            self._load_player_data()
            
            return {
                "ok": True,
                "data": self.player_data
            }
        except Exception as e:
            logger.error(f"Error al obtener datos del jugador: {e}")
            return {"ok": False, "message": f"Error: {str(e)}"}
    
    def get_key_data(self):
        """Obtiene información sobre la clave de acceso"""
        try:
            response = self.session.get(f"{self.base_url}/key_data")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("ok", False):
                    return data.get("data", {})
                else:
                    logger.warning(f"No se pudo obtener info de la clave: {data.get('message')}")
                    return {}
            else:
                logger.error(f"Error HTTP {response.status_code} al obtener info de la clave")
                return {}
        except Exception as e:
            logger.error(f"Error al obtener info de la clave: {e}")
            return {}
    
    def set_player_money(self, amount):
        """Establece la cantidad de dinero del jugador"""
        if not self.logged_in:
            logger.warning("Intento de establecer dinero sin iniciar sesión")
            return False
        
        try:
            response = self.session.post(
                f"{self.base_url}/set_money", 
                json={"amount": amount}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("ok", False):
                    # Actualizamos el valor local
                    if self.player_data:
                        self.player_data["money"] = amount
                    logger.info(f"Dinero actualizado correctamente a: {amount}")
                    return True
                else:
                    logger.warning(f"No se pudo actualizar el dinero: {data.get('message')}")
                    return False
            else:
                logger.error(f"Error HTTP {response.status_code} al actualizar dinero")
                return False
        except Exception as e:
            logger.error(f"Error al establecer dinero del jugador: {e}")
            return False
    
    def set_player_coins(self, amount):
        """Establece la cantidad de monedas del jugador"""
        if not self.logged_in:
            logger.warning("Intento de establecer monedas sin iniciar sesión")
            return False
        
        try:
            response = self.session.post(
                f"{self.base_url}/set_coins", 
                json={"amount": amount}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("ok", False):
                    # Actualizamos el valor local
                    if self.player_data:
                        self.player_data["coin"] = amount
                    logger.info(f"Monedas actualizadas correctamente a: {amount}")
                    return True
                else:
                    logger.warning(f"No se pudieron actualizar las monedas: {data.get('message')}")
                    return False
            else:
                logger.error(f"Error HTTP {response.status_code} al actualizar monedas")
                return False
        except Exception as e:
            logger.error(f"Error al establecer monedas del jugador: {e}")
            return False
    
    def set_player_rank(self):
        """Establece el rango del jugador a Rey"""
        if not self.logged_in:
            logger.warning("Intento de establecer rango sin iniciar sesión")
            return False
        
        try:
            response = self.session.post(f"{self.base_url}/set_rank", json={"rank": "Rey"})
            
            if response.status_code == 200:
                data = response.json()
                if data.get("ok", False):
                    logger.info("Rango actualizado correctamente a Rey")
                    return True
                else:
                    logger.warning(f"No se pudo actualizar el rango: {data.get('message')}")
                    return False
            else:
                logger.error(f"Error HTTP {response.status_code} al actualizar rango")
                return False
        except Exception as e:
            logger.error(f"Error al establecer rango del jugador: {e}")
            return False
    
    def set_player_localid(self, new_id):
        """Cambia el ID local del jugador"""
        if not self.logged_in:
            logger.warning("Intento de cambiar ID local sin iniciar sesión")
            return False
        
        try:
            response = self.session.post(
                f"{self.base_url}/set_localid", 
                json={"localid": new_id}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("ok", False):
                    # Actualizamos el valor local
                    if self.player_data:
                        self.player_data["localID"] = new_id
                    logger.info(f"ID local actualizado correctamente a: {new_id}")
                    return True
                else:
                    logger.warning(f"No se pudo actualizar el ID local: {data.get('message')}")
                    return False
            else:
                logger.error(f"Error HTTP {response.status_code} al actualizar ID local")
                return False
        except Exception as e:
            logger.error(f"Error al cambiar ID local del jugador: {e}")
            return False
    
    def set_player_name(self, new_name):
        """Cambia el nombre del jugador"""
        if not self.logged_in:
            logger.warning("Intento de cambiar nombre sin iniciar sesión")
            return False
        
        try:
            response = self.session.post(
                f"{self.base_url}/set_name", 
                json={"name": new_name}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("ok", False):
                    # Actualizamos el valor local
                    if self.player_data:
                        self.player_data["Name"] = new_name
                    logger.info(f"Nombre actualizado correctamente a: {new_name}")
                    return True
                else:
                    logger.warning(f"No se pudo actualizar el nombre: {data.get('message')}")
                    return False
            else:
                logger.error(f"Error HTTP {response.status_code} al actualizar nombre")
                return False
        except Exception as e:
            logger.error(f"Error al cambiar nombre del jugador: {e}")
            return False
    
    def modificar_todos_los_autos(self, hp, hp_interno, nm, torque):
        """Modifica todos los autos con los parámetros especificados"""
        if not self.logged_in:
            logger.warning("Intento de modificar autos sin iniciar sesión")
            return False
        
        try:
            # Preparamos los datos para la solicitud
            car_data = {
                "hp": hp,
                "hp_interno": hp_interno,
                "nm": nm,
                "torque": torque
            }
            
            response = self.session.post(f"{self.base_url}/modify_all_cars", json=car_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("ok", False):
                    logger.info("Todos los autos modificados correctamente")
                    return True
                else:
                    logger.warning(f"No se pudieron modificar los autos: {data.get('message')}")
                    return False
            else:
                logger.error(f"Error HTTP {response.status_code} al modificar autos")
                return False
        except Exception as e:
            logger.error(f"Error al modificar todos los autos: {e}")
            return False
    
    def logout(self):
        """Cierra la sesión del usuario"""
        if not self.logged_in:
            return True
        
        try:
            response = self.session.post(f"{self.base_url}/logout")
            self.logged_in = False
            self.player_data = None
            logger.info("Sesión cerrada correctamente")
            return True
        except Exception as e:
            logger.error(f"Error al cerrar sesión: {e}")
            return False

# Token del bot
BOT_TOKEN = '7912969152:AAFaIvqm39uPL2C7PXS2xInVITo-TwZ_F-8'

# Ejemplo de uso
if __name__ == '__main__':
    # Este código se ejecutará si ejecutas directamente este archivo
    print("Módulo leunamcpm cargado correctamente")
    print(f"Token del bot configurado: {BOT_TOKEN}")
    
    # Ejemplo básico de cómo usar la clase (descomentar para probar)
    """
    cpm = leunamcpm("tu_clave_de_acceso")
    resultado = cpm.login("tu_email", "tu_contraseña")
    if resultado == 0:
        print("Inicio de sesión exitoso")
        print(cpm.get_player_data())
    else:
        print(f"Error al iniciar sesión: {resultado}")
    """
