import re
import time

import pyautogui
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.webdriver_actions.html_actions import webdriver_actions_constantes


class ValidacionesHtml():

    @staticmethod
    def verificar_elemento_html_por_id(id: str, web_driver: WebDriver):

        try:
            web_driver.find_element(By.ID, id)
            return True
        except NoSuchElementException:
            return False

    @staticmethod
    def verificar_elemento_html_por_class_name(class_name: str, web_driver: WebDriver):

        try:
            web_driver.find_element(By.CLASS_NAME, class_name)
            return True
        except NoSuchElementException:
            return False

    @staticmethod
    def verificar_elemento_html_por_xpath(xpath: str, web_driver: WebDriver):

        try:
            web_driver.find_element(By.XPATH, xpath)
            return True
        except NoSuchElementException:
            return False

    @staticmethod
    def se_encuentran_mas_ventanas_en_sesion(web_driver: WebDriver, tiempo_espera: int):
        count = 0
        while count < tiempo_espera:
            if len(web_driver.window_handles) > 1:
                return True
            else:
                count = count + 1

            time.sleep(1)

        driver_excep = WebDriverException('Han transcurrido mas de {} seg. sin obtener la nueva ventana de '
                                          'inicio de sesion mediante Gmail'.format(tiempo_espera))

        raise TimeoutException(driver_excep)

    @staticmethod
    def verificar_remover_ventana_configuracion(web_driver: WebDriver):

        try:
            btn_cierre_ventana_configuracion = WebDriverWait(web_driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'continuous-onboarding-collapse-btn')))
            btn_cierre_ventana_configuracion.click()
        except TimeoutException:
            pass

    @staticmethod
    def verificar_archivo_ya_existente_en_portal(web_driver: WebDriver, nombre_archivo_sin_ext: str):

        try:
            lista_archivos_actuales = web_driver.find_elements(By.XPATH, '//div[@data-item-id]')

            if len(lista_archivos_actuales) > 0:
                for div_archivo in lista_archivos_actuales:
                    div_recent_item_header = div_archivo.find_element(By.CLASS_NAME, 'recents-item-header')
                    div_recent_item_header_content = div_recent_item_header.find_element(By.CLASS_NAME,
                                                                                         'recents-item-header__content')
                    link_nombre_archivo = div_recent_item_header_content.find_element(By.TAG_NAME, 'a')

                    if link_nombre_archivo.text.strip() == nombre_archivo_sin_ext.strip():
                        div_item_actions = WebDriverWait(web_driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'recents-item__actions')))

                        WebDriverWait(div_item_actions, 10).until(
                            EC.element_to_be_clickable((By.CLASS_NAME, 'dig-IconButton-content')))

                        btn_mas = div_item_actions.find_element_by_class_name('dig-IconButton-content')
                        btn_mas.click()

                        sub_menu_acciones = WebDriverWait(web_driver, 10).until(
                            EC.element_to_be_clickable((By.CLASS_NAME, 'dig-Layer')))

                        btn_eliminar = WebDriverWait(sub_menu_acciones, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//span[text()="Eliminar…"]')))

                        btn_eliminar.click()

                        modal_eliminacion = WebDriverWait(web_driver, 10).until(
                            EC.element_to_be_clickable((By.CLASS_NAME, 'db-modal-box')))

                        btn_eliminacion_definitivo = WebDriverWait(modal_eliminacion, 10).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, '//button[@class="button-primary dbmodal-button"][text()="Eliminar"]')))

                        btn_eliminacion_definitivo.click()

                        WebDriverWait(web_driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, '//span[@id="notify-msg"]')))

        except ElementNotInteractableException as e:
            pass
        except NoSuchElementException:
            pass
        except TimeoutException:
            pass
        except ElementClickInterceptedException:
            pass

    @staticmethod
    def verificar_mensaje_de_carga_exitosa_de_archivo(web_driver: WebDriver, nombre_archivo_a_cargar: str,
                                                      numero_de_seg_en_espera: int = 720):
        segundos_transcurridos = 0

        while segundos_transcurridos < numero_de_seg_en_espera:

            list_modal_mensaje_upload = web_driver.find_elements(By.CLASS_NAME, 'dig-Layer')

            if len(list_modal_mensaje_upload) > 0:
                modal = list_modal_mensaje_upload[0]

                list_spans_es = modal.find_elements(By.XPATH, '//span[text()="1 carga completada"]')
                list_spans_en = modal.find_elements(By.XPATH, '//span[text()="1 upload complete"]')

                if len(list_spans_es) > 0 or len(list_spans_en) > 0:
                    break

            time.sleep(1)
            segundos_transcurridos += 1

        if segundos_transcurridos == numero_de_seg_en_espera:
            e = TimeoutException()
            e.msg = webdriver_actions_constantes.WEBDRIVER_WAIT_TIMEOUT_EXCEPTION.format(
                segundos_transcurridos,
                'span con el texto de finalizacion de carga de archivo dentro del portal drop box.',
                '')
            raise e

    @staticmethod
    def cerrar_mensaje_carga_completa(web_driver: WebDriver, intentos: int = 3):

        intentos_ejecutados = 0

        while intentos_ejecutados < intentos:

            try:
                list_btn_cross = web_driver.find_elements(
                    By.XPATH, '//button[@data-testid="rich-snackbar-close-btn"]')

                list_btn_cerrar = web_driver.find_elements(
                    By.XPATH, '//span[@class="dig-Button-content"][text()="Cerrar"]')

                exist_btn_cerrar = len(list_btn_cerrar) > 0
                exist_btn_cross = len(list_btn_cross) > 0

                if exist_btn_cerrar:
                    btn = list_btn_cerrar[0]
                    btn.click()

                if exist_btn_cross:
                    btn = list_btn_cross[0]
                    btn.click()

                intentos_ejecutados += 1
            except ElementNotInteractableException:
                intentos_ejecutados += 1
            except TimeoutException:
                intentos_ejecutados += 1
            except ElementClickInterceptedException:
                intentos_ejecutados += 1
            except NoSuchElementException:
                intentos_ejecutados += 1

    @staticmethod
    def establecer_carga_de_archivo(web_driver: WebDriver, path_archivo_por_cargar: str):

        # screenWidth, screenHeight = pyautogui.size()

        # print('ancho: {}'.format(screenWidth))
        # print('altura: {}'.format(screenHeight))

        time.sleep(6)
        # da clic en other locations
        pyautogui.moveTo(80, 205)
        pyautogui.click()
        time.sleep(3)

        # da clic en computer
        pyautogui.moveTo(233, 78)
        pyautogui.click()
        time.sleep(3)

        # da clic en la imagen
        pyautogui.moveTo(213, 289)
        pyautogui.click()
        time.sleep(3)

        # da clic en el boton de open
        pyautogui.moveTo(1076, 822)
        pyautogui.click()
        time.sleep(3)

    @staticmethod
    def validacion_eliminacion_fichero(web_driver: WebDriver,
                                       tiempo_de_espera: int = 30):

        # validacion de elimiinacion de fichero
        tiempo_transcurrido_en_segundos = 0
        se_localizo_elemento = False

        while tiempo_transcurrido_en_segundos < tiempo_de_espera:
            try:
                div_msg = web_driver.find_element(By.CLASS_NAME, 'dig-Snackbar-message')

                msg_eliminacion = div_msg.get_attribute('innerText').strip()

                if msg_eliminacion == 'Se elimin\u00F3 1 elemento.' \
                        or re.search('^Se elimin\u00F3*', msg_eliminacion) \
                        or msg_eliminacion == 'Deleted 1 item.':
                    se_localizo_elemento = True
                    break

            except NoSuchElementException:
                se_localizo_elemento = False

            time.sleep(1)
            tiempo_transcurrido_en_segundos += 1

        if not se_localizo_elemento:
            e = TimeoutException()
            e.msg = webdriver_actions_constantes.WEBDRIVER_WAIT_TIMEOUT_EXCEPTION.format(
                tiempo_de_espera,
                'div con la clase css dig-Snackbar-message.',
                '')
            raise e
