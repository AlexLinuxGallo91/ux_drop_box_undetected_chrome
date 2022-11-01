import time
from os import path
from pathlib import Path

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver

from src.step_evaluaciones import constantes_evaluaciones_claro_drive as const
from src.utils.utils_evaluaciones import UtilsEvaluaciones
from src.utils.utils_format import FormatUtils
from src.utils.utils_html import ValidacionesHtml
from src.utils.utils_temporizador import Temporizador
from src.webdriver_actions.html_actions import HtmlActions


class EvaluacionesDropBoxDriveSteps:

    def ingreso_pagina_principal_dropbox(self, webdriver_test_ux: WebDriver, json_eval, url_login):
        tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        webdriver_test_ux.get(url_login)

        try:
            time.sleep(const.TIMEOUT_STEP_INGRESO_PAGINA_PRINCIPAL_INICIALIZACION_WEBDRIVER)

            # verifica que no estemos loggeados desde un inicio, en caso contrario, cerramos sesion
            if ValidacionesHtml.verificar_elemento_html_por_id(
                    const.HTML_STEP_INGRESO_PAGINA_ID_PORTAL_PRINCIPAL, webdriver_test_ux):

                boton_imagen_perfil = HtmlActions.webdriver_wait_element_to_be_clickable(
                    webdriver_test_ux,
                    const.TIMEOUT_STEP_INGRESO_PAGINA_PRINCIPAL_BOTON_IMG_PERFIL,
                    class_name=const.HTML_STEP_INGRESO_PAGINA_CLASS_NAME_BOTON_PERFIL_USUARIO)

                HtmlActions.click_html_element(
                    boton_imagen_perfil, class_name=const.HTML_STEP_INGRESO_PAGINA_CLASS_NAME_BOTON_PERFIL_USUARIO)

                boton_salir_sesion = HtmlActions.webdriver_wait_element_to_be_clickable(
                    webdriver_test_ux, const.TIMEOUT_STEP_INGRESO_PAGINA_PRINCIPAL_BOTON_SALIR_SESION,
                    xpath=const.HTML_STEP_INGRESO_PAGINA_XPATH_BOTON_CIERRE_DE_SESION)

                HtmlActions.click_html_element(
                    boton_salir_sesion, xpath=const.HTML_STEP_INGRESO_PAGINA_XPATH_BOTON_CIERRE_DE_SESION)

            else:
                webdriver_test_ux.get(url_login)

            HtmlActions.webdriver_wait_presence_of_element_located(
                webdriver_test_ux, const.TIMEOUT_STEP_INGRESO_PAGINA_PRINCIPAL_INPUT_LOGIN_EMAIL,
                name=const.HTML_STEP_INGRESO_PAGINA_NAME_INPUT_LOGIN_EMAIL)

            HtmlActions.webdriver_wait_presence_of_element_located(
                webdriver_test_ux, const.TIMEOUT_STEP_INGRESO_PAGINA_PRINCIPAL_INPUT_LOGIN_PASSWORD,
                name=const.HTML_STEP_INGRESO_PAGINA_NAME_INPUT_LOGIN_PASSWORD)

            json_eval = UtilsEvaluaciones.establecer_output_status_step(
                json_eval, 0, 0, True, const.MSG_OUTPUT_INGRESO_PAGINA_PRINCIPAL_EXITOSO)

        except ElementNotInteractableException as e:
            msg_output = const.MSG_OUTPUT_INGRESO_PAGINA_PRINCIPAL_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 0, 0, False, msg_output)

        except NoSuchElementException as e:
            msg_output = const.MSG_OUTPUT_INGRESO_PAGINA_PRINCIPAL_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 0, 0, False, msg_output)

        except TimeoutException as e:
            msg_output = const.MSG_OUTPUT_INGRESO_PAGINA_PRINCIPAL_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 0, 0, False, msg_output)

        except ElementClickInterceptedException as e:
            msg_output = const.MSG_OUTPUT_INGRESO_PAGINA_PRINCIPAL_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 0, 0, False, msg_output)

        except WebDriverException as e:
            msg_output = const.MSG_OUTPUT_INGRESO_PAGINA_PRINCIPAL_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 0, 0, False, msg_output)

        json_eval = UtilsEvaluaciones.finalizar_tiempos_en_step(json_eval, 0, tiempo_step_inicio, fecha_inicio)

        return json_eval

    def inicio_sesion_dropbox(self, webdriver_test_ux: WebDriver, json_eval, json_args, url_login):
        tiempo_step_inicio = None
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        if not UtilsEvaluaciones.se_ingreso_correctamente_a_la_pagina_principal(json_eval):
            json_eval = UtilsEvaluaciones.generar_json_inicio_de_sesion_incorrecta(
                json_eval, tiempo_step_inicio, fecha_inicio, 1,
                const.MSG_INICIO_SESION_FALLIDA_POR_INGRESO_DE_PAGINA)

            return json_eval

        try:

            # valida si se ingresara por medio de correo o por gmail
            archivo_config_ini = FormatUtils.lector_archivo_ini()
            bandera_ingreso_correo = archivo_config_ini.getboolean('path_and_credentials', 'ingreso_por_gmail')

            if not bandera_ingreso_correo:

                email_input = HtmlActions.webdriver_wait_element_to_be_clickable(
                    webdriver_test_ux, const.TIMEOUT_STEP_INICIO_SESION_DROP_BOX_BOTON_INICIO_SESION_GMAIL,
                    name='login_email')

                HtmlActions.enviar_data_keys(email_input, json_args['user'], name='login_email')

                password_input = HtmlActions.webdriver_wait_element_to_be_clickable(
                    webdriver_test_ux, const.TIMEOUT_STEP_INICIO_SESION_DROP_BOX_BOTON_INICIO_SESION_GMAIL,
                    name='login_password')

                HtmlActions.enviar_data_keys(password_input, json_args['password'], name='login_password')

                btn_inicio_sesion = HtmlActions.webdriver_wait_element_to_be_clickable(
                    webdriver_test_ux, const.TIMEOUT_STEP_INICIO_SESION_DROP_BOX_BOTON_INICIO_SESION_GMAIL,
                    class_name='signin-text')

                btn_inicio_sesion.click()

            else:

                btn_inicio_sesion = HtmlActions.webdriver_wait_element_to_be_clickable(
                    webdriver_test_ux, const.TIMEOUT_STEP_INICIO_SESION_DROP_BOX_BOTON_INICIO_SESION_GMAIL,
                    xpath=const.HTML_STEP_INICIO_SESION_XPATH_BTN_INICIO_SESION)

                HtmlActions.click_html_element(
                    btn_inicio_sesion, xpath=const.HTML_STEP_INICIO_SESION_XPATH_BTN_INICIO_SESION)

                if ValidacionesHtml.se_encuentran_mas_ventanas_en_sesion(
                        webdriver_test_ux, const.TIMEOUT_STEP_INICIO_SESION_DROP_BOX_VENTANAS_EN_SESION):
                    ventana_padre = webdriver_test_ux.window_handles[0]
                    ventana_hija = webdriver_test_ux.window_handles[1]

                    webdriver_test_ux.switch_to.window(ventana_hija)

                view_container = HtmlActions.webdriver_wait_presence_of_element_located(
                    webdriver_test_ux, const.TIMEOUT_STEP_INICIO_SESION_DROP_BOX_VIEW_CONTAINER,
                    id=const.HTML_STEP_INICIO_SESION_ID_INITIAL_VIEW)

                input_email_gmail = HtmlActions.webdriver_wait_element_to_be_clickable(
                    view_container, const.TIMEOUT_STEP_INICIO_SESION_DROP_BOX_INPUT_EMAIL,
                    id=const.HTML_STEP_INICIO_SESION_ID_INPUT_EMAIL)

                HtmlActions.enviar_data_keys(
                    input_email_gmail, json_args['user'], id=const.HTML_STEP_INICIO_SESION_ID_INPUT_EMAIL)

                btn_next = HtmlActions.webdriver_wait_element_to_be_clickable(
                    view_container, const.TIMEOUT_STEP_INICIO_SESION_DROP_BOX_BOTON_NEXT,
                    id=const.HTML_STEP_INICIO_SESION_ID_BTN_NEXT)

                HtmlActions.click_html_element(btn_next, id=const.HTML_STEP_INICIO_SESION_ID_BTN_NEXT)

                div_password_gmail = HtmlActions.webdriver_wait_presence_of_element_located(
                    webdriver_test_ux, time=12, id=const.HTML_STEP_INICIO_SESION_ID_DIV_PASSWORD_GMAIL)

                input_password_gmail = HtmlActions.webdriver_wait_element_to_be_clickable(
                    div_password_gmail, time=12, name=const.HTML_STEP_INICIO_SESION_NAME_INPUT_PASSWORD_GMAIL)

                input_password_gmail.clear()

                HtmlActions.enviar_data_keys(
                    input_password_gmail, json_args['password'],
                    name=const.HTML_STEP_INICIO_SESION_NAME_INPUT_PASSWORD_GMAIL)

                time.sleep(2)

                boton_inicio_de_sesion = HtmlActions.webdriver_wait_presence_of_element_located(
                    webdriver_test_ux, id=const.HTML_STEP_INICIO_SESION_ID_BTN_INICIO_DE_SESION)

                HtmlActions.click_html_element(
                    boton_inicio_de_sesion, id=const.HTML_STEP_INICIO_SESION_ID_BTN_INICIO_DE_SESION)

                tiempo_step_inicio = Temporizador.obtener_tiempo_timer()

                webdriver_test_ux.switch_to.window(ventana_padre)

            HtmlActions.webdriver_wait_element_to_be_clickable(
                webdriver_test_ux, const.TIMEOUT_STEP_INICIO_SESION_DROP_BOX_PORTAL_PRINCIPAL,
                class_name=const.HTML_STEP_INICIO_SESION_CLASS_NAME_DIV_MAESTRO_PORTAL)

            # verifica el lenguaje del portal
            lang_tag = HtmlActions.webdriver_wait_presence_of_element_located(
                webdriver_test_ux, 10, tag_name='html')

            const.LANG = lang_tag.get_attribute('lang')

            json_eval = UtilsEvaluaciones.establecer_output_status_step(
                json_eval, 1, 0, True, const.MSG_OUTPUT_INICIO_SESION_EXITOSO)

        except ElementNotInteractableException as e:
            msg_output = const.MSG_OUTPUT_INICIO_SESION_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 1, 0, False, msg_output)

        except NoSuchElementException as e:
            msg_output = const.MSG_OUTPUT_INICIO_SESION_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 1, 0, False, msg_output)

        except TimeoutException as e:
            msg_output = const.MSG_OUTPUT_INICIO_SESION_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 1, 0, False, msg_output)

        except ElementClickInterceptedException as e:
            msg_output = const.MSG_OUTPUT_INICIO_SESION_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 1, 0, False, msg_output)

        json_eval = UtilsEvaluaciones.finalizar_tiempos_en_step(json_eval, 1, tiempo_step_inicio, fecha_inicio)

        return json_eval

    def cargar_archivo_dropbox(self, webdriver_test_ux: WebDriver, json_eval, json_args, nombre_archivo_sin_ext,
                               nombre_archivo_con_ext):
        tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        if not UtilsEvaluaciones.se_ingreso_correctamente_a_la_sesion(json_eval):
            json_eval = UtilsEvaluaciones.generar_json_inicio_de_sesion_incorrecta(
                json_eval, tiempo_step_inicio, fecha_inicio, 2,
                const.MSG_CARGA_ARCHIVO_FALLIDA_POR_INICIO_DE_SESION)

            return json_eval

        try:
            ValidacionesHtml.verificar_remover_ventana_configuracion(webdriver_test_ux)
            ValidacionesHtml.verificar_archivo_ya_existente_en_portal(webdriver_test_ux, nombre_archivo_sin_ext)

            # se ingresa a la pagina principal del portal
            webdriver_test_ux.get(const.HTML_STEP_CARGAR_ARCHIVO_URL_ROLE_PERSONAL)

            maestro_content_portal = HtmlActions.webdriver_wait_presence_of_element_located(
                webdriver_test_ux, const.TIMEOUT_STEP_CARGA_ARCHIVO_VALIDACION_ELEMENTO_MAESTRO_CONTENT_PORTAL,
                id=const.HTML_STEP_CARGAR_ARCHIVO_ID_MAESTRO_CONTENT_PORTAL)

            div_botones_carga = HtmlActions.webdriver_wait_element_to_be_clickable(
                maestro_content_portal, const.TIMEOUT_STEP_CARGA_ARCHIVO_VALIDACION_BOTON_CARGA_DE_ARCHIVO,
                class_name='files-page-action-bar-container')

            btn_carga = HtmlActions.webdriver_wait_element_to_be_clickable(
                div_botones_carga, const.TIMEOUT_STEP_CARGA_ARCHIVO_VALIDACION_BOTON_CARGA_DE_ARCHIVO,
                class_name='rc-action-bar-top-level')

            HtmlActions.click_html_element(btn_carga, class_name=const.HTML_STEP_CARGAR_ARCHIVO_CLASS_NAME_BTN_CARGA)

            btn_files = HtmlActions.webdriver_wait_element_to_be_clickable(
                div_botones_carga, const.TIMEOUT_STEP_CARGA_ARCHIVO_VALIDACION_BOTON_CARGA_DE_ARCHIVO,
                xpath=const.HTML_STEP_CARGAR_ARCHIVO_XPATH_BTN_FILES_EN if const.LANG == 'en' else
                const.HTML_STEP_CARGAR_ARCHIVO_XPATH_BTN_FILES_ES)

            HtmlActions.click_html_element(btn_files, class_name=const.HTML_STEP_CARGAR_ARCHIVO_CLASS_NAME_BTN_CARGA)

            ValidacionesHtml.establecer_carga_de_archivo(webdriver_test_ux, json_args['pathImage'])

            div_modal_footer = HtmlActions.webdriver_wait_element_to_be_clickable(
                webdriver_test_ux, const.TIMEOUT_STEP_CARGA_ARCHIVO_BTN_UPLOAD,
                class_name=const.HTML_STEP_CARGAR_ARCHIVO_CLASS_NAME_BTN_UPLOAD)

            btn_upload = HtmlActions.webdriver_wait_element_to_be_clickable(
                div_modal_footer, const.TIMEOUT_STEP_CARGA_ARCHIVO_VALIDACION_BOTON_CARGA_DE_ARCHIVO,
                class_name='dig-Button--primary')

            btn_upload.click()

            ValidacionesHtml.verificar_mensaje_de_carga_exitosa_de_archivo(
                webdriver_test_ux, nombre_archivo_con_ext, const.TIMEOUT_STEP_CARGA_ARCHIVO_VERIFICACION_CARGA_EXITOSA)

            json_eval = UtilsEvaluaciones.establecer_output_status_step(
                json_eval, 2, 0, True, const.MSG_OUTPUT_CARGA_ARCHIVO_EXITOSO)

        except ElementNotInteractableException as e:
            msg_output = const.MSG_OUTPUT_CARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 2, 0, False, msg_output)

        except NoSuchElementException as e:
            msg_output = const.MSG_OUTPUT_CARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 2, 0, False, msg_output)

        except TimeoutException as e:
            msg_output = const.MSG_OUTPUT_CARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 2, 0, False, msg_output)

        except ElementClickInterceptedException as e:
            msg_output = const.MSG_OUTPUT_CARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 2, 0, False, msg_output)

        json_eval = UtilsEvaluaciones.finalizar_tiempos_en_step(json_eval, 2, tiempo_step_inicio, fecha_inicio)

        return json_eval

    def descargar_archivo_dropbox(self, webdriver_test_ux: WebDriver, json_eval, nombre_archivo_con_ext):
        extension_del_archivo = path.splitext(nombre_archivo_con_ext)[1]
        nombre_del_archivo_sin_extension = Path(nombre_archivo_con_ext).stem

        tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        if not UtilsEvaluaciones.se_ingreso_correctamente_a_la_sesion(json_eval):
            json_eval = UtilsEvaluaciones.generar_json_inicio_de_sesion_incorrecta(
                json_eval, tiempo_step_inicio, fecha_inicio, 3,
                const.MSG_DESCARGA_ARCHIVO_FALLIDA_POR_CARGA_ARCHIVO_FALLIDA)

            return json_eval

        try:
            ValidacionesHtml.verificar_remover_ventana_configuracion(webdriver_test_ux)

            search_bar = HtmlActions.webdriver_wait_element_to_be_clickable(
                webdriver_test_ux, const.TIMEOUT_STEP_DESCARGA_ARCHIVO_BARRA_BUSQUEDA,
                class_name=const.HTML_STEP_DESCARGA_ARCHIVO_CLASS_NAME_SEARCH_BAR)

            HtmlActions.enviar_data_keys(
                search_bar, nombre_archivo_con_ext, class_name=const.HTML_STEP_DESCARGA_ARCHIVO_CLASS_NAME_SEARCH_BAR)

            HtmlActions.enviar_data_keys(
                search_bar, Keys.RETURN, class_name=const.HTML_STEP_DESCARGA_ARCHIVO_CLASS_NAME_SEARCH_BAR)

            archivo_por_descargar = HtmlActions.webdriver_wait_element_to_be_clickable(
                webdriver_test_ux, const.TIMEOUT_STEP_DESCARGA_ARCHIVO_ELEM_HTML_ARCHIVO_POR_DESCARGAR,
                xpath=const.HTML_STEP_DESCARGA_ARCHIVO_XPATH_ARCHIVO_POR_DESCARGAR.format(nombre_archivo_con_ext))

            checkbox = HtmlActions.webdriver_wait_element_to_be_clickable(
                archivo_por_descargar, const.TIMEOUT_STEP_DESCARGA_ARCHIVO_CHECKBOX_ARCHIVO_POR_DESCARGAR,
                class_name=const.HTML_STEP_DESCARGA_ARCHIVO_CLASS_NAME_CHECKBOX)

            HtmlActions.click_html_element(checkbox, class_name=const.HTML_STEP_DESCARGA_ARCHIVO_CLASS_NAME_CHECKBOX)

            btn_mas_acciones = HtmlActions.webdriver_wait_element_to_be_clickable(
                archivo_por_descargar, const.TIMEOUT_STEP_DESCARGA_ARCHIVO_BOTON_MAS_ACCIONES,
                xpath=const.HTML_STEP_DESCARGA_ARCHIVO_XPATH_BTN_MAS_ACCIONES)

            HtmlActions.click_html_element(
                btn_mas_acciones, xpath=const.HTML_STEP_DESCARGA_ARCHIVO_XPATH_BTN_MAS_ACCIONES)

            btn_descargar = HtmlActions.webdriver_wait_element_to_be_clickable(
                webdriver_test_ux, const.TIMEOUT_STEP_DESCARGA_ARCHIVO_BOTON_DESCARGAR,
                xpath=const.HTML_STEP_DESCARGA_ARCHIVO_XPATH_BTN_DESCARGAR_ES if const.LANG == 'es'
                else const.HTML_STEP_DESCARGA_ARCHIVO_XPATH_BTN_DESCARGAR_EN)

            HtmlActions.click_html_element(
                btn_descargar, xpath=const.HTML_STEP_DESCARGA_ARCHIVO_XPATH_BTN_DESCARGAR_ES
                if const.LANG == 'es' else const.HTML_STEP_DESCARGA_ARCHIVO_XPATH_BTN_DESCARGAR_EN)

            UtilsEvaluaciones.verificar_descarga_en_ejecucion(
                nombre_del_archivo_sin_extension, extension_del_archivo,
                const.TIMEOUT_STEP_DESCARGA_ARCHIVO_VERIFICAR_TIEMPO_DESCARGA)

            json_eval = UtilsEvaluaciones.establecer_output_status_step(
                json_eval, 3, 0, True, const.MSG_OUTPUT_DESCARGA_ARCHIVO_EXITOSO)

        except ElementNotInteractableException as e:
            msg_output = const.MSG_OUTPUT_DESCARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 3, 0, False, msg_output)

        except NoSuchElementException as e:
            msg_output = const.MSG_OUTPUT_DESCARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 3, 0, False, msg_output)

        except TimeoutException as e:
            msg_output = const.MSG_OUTPUT_DESCARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 3, 0, False, msg_output)

        except ElementClickInterceptedException as e:
            msg_output = const.MSG_OUTPUT_DESCARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 3, 0, False, msg_output)

        except StaleElementReferenceException as e:
            msg_output = const.MSG_OUTPUT_DESCARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 3, 0, False, msg_output)

        json_eval = UtilsEvaluaciones.finalizar_tiempos_en_step(json_eval, 3, tiempo_step_inicio, fecha_inicio)

        return json_eval

    def eliminar_archivo_dropbox(self, webdriver_test_ux: WebDriver, json_eval, nombre_archivo_con_ext):
        tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        if not UtilsEvaluaciones.se_ingreso_correctamente_a_la_sesion(json_eval):
            json_eval = UtilsEvaluaciones.generar_json_inicio_de_sesion_incorrecta(
                json_eval, tiempo_step_inicio, fecha_inicio, 4,
                const.MSG_ELIMINACION_ARCHIVO_FALLIDA_POR_CARGA_ARCHIVO_FALLIDA)

            return json_eval

        try:

            archivo_por_eliminar = HtmlActions.webdriver_wait_element_to_be_clickable(
                webdriver_test_ux, const.TIMEOUT_STEP_ELIMINACION_ARCHIVO_ELEM_ARCHIVO_POR_ELIMINAR,
                xpath=const.HTML_STEP_ELIMINAR_ARCHIVO_XPATH_ARCHIVO_POR_ELIMINAR.format(nombre_archivo_con_ext))

            btn_eliminar = HtmlActions.webdriver_wait_element_to_be_clickable(
                webdriver_test_ux, const.TIMEOUT_STEP_ELIMINACION_ARCHIVO_BOTON_MAS_ACCIONES,
                class_name='action-bar-action-6')

            HtmlActions.click_html_element(btn_eliminar, class_name='action-bar-action-6')

            modal_eliminacion = HtmlActions.webdriver_wait_element_to_be_clickable(
                webdriver_test_ux, const.TIMEOUT_STEP_ELIMINACION_ARCHIVO_BOTON_MAS_ACCIONES,
                class_name='dig-Modal-footer')

            btn_eliminar_modal = HtmlActions.webdriver_wait_element_to_be_clickable(
                modal_eliminacion, const.TIMEOUT_STEP_ELIMINACION_ARCHIVO_BOTON_MAS_ACCIONES,
                class_name='dig-Button--primary')

            HtmlActions.click_html_element(btn_eliminar_modal, class_name='dig-Button--primary')

            ValidacionesHtml.validacion_eliminacion_fichero(webdriver_test_ux, 30)

            json_eval = UtilsEvaluaciones.establecer_output_status_step(
                json_eval, 4, 0, True, const.MSG_OUTPUT_BORRADO_ARCHIVO_EXITOSO)

        except ElementNotInteractableException as e:
            msg_output = const.MSG_OUTPUT_BORRADO_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 4, 0, False, msg_output)

        except NoSuchElementException as e:
            msg_output = const.MSG_OUTPUT_BORRADO_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 4, 0, False, msg_output)

        except TimeoutException as e:
            msg_output = const.MSG_OUTPUT_BORRADO_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 4, 0, False, msg_output)

        except ElementClickInterceptedException as e:
            msg_output = const.MSG_OUTPUT_BORRADO_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 4, 0, False, msg_output)

        json_eval = UtilsEvaluaciones.finalizar_tiempos_en_step(json_eval, 4, tiempo_step_inicio, fecha_inicio)

        return json_eval

    def cerrar_sesion_dropbox(self, webdriver_test_ux: WebDriver, json_eval):
        tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        if not UtilsEvaluaciones.se_ingreso_correctamente_a_la_sesion(json_eval):
            json_eval = UtilsEvaluaciones.generar_json_inicio_de_sesion_incorrecta(
                json_eval, tiempo_step_inicio, fecha_inicio, 5,
                const.MSG_CIERRE_SESION_FALLIDA_POR_INICIO_DE_SESION)

            return json_eval

        try:
            boton_imagen_perfil = HtmlActions.webdriver_wait_element_to_be_clickable(
                webdriver_test_ux, const.TIMEOUT_STEP_CIERRE_DE_SESION_BOTON_IMAGEN_PERFIL,
                class_name=const.HTML_STEP_CERRAR_SESION_CLASS_NAME_BTN_IMAGEN_PERFIL)

            HtmlActions.click_html_element(
                boton_imagen_perfil, class_name=const.HTML_STEP_CERRAR_SESION_CLASS_NAME_BTN_IMAGEN_PERFIL)

            boton_cerrar_sesion = HtmlActions.webdriver_wait_element_to_be_clickable(
                webdriver_test_ux, const.TIMEOUT_STEP_CIERRE_DE_SESION_BOTON_SALIR_SESION,
                xpath=const.HTML_STEP_CERRAR_SESION_XPATH_BTN_CERRAR_SESION_ES if const.LANG == 'es' else
                const.HTML_STEP_CERRAR_SESION_XPATH_BTN_CERRAR_SESION_EN)

            HtmlActions.click_html_element(
                boton_cerrar_sesion,
                xpath=const.HTML_STEP_CERRAR_SESION_XPATH_BTN_CERRAR_SESION_ES if const.LANG == 'es' else
                const.HTML_STEP_CERRAR_SESION_XPATH_BTN_CERRAR_SESION_EN)

            HtmlActions.webdriver_wait_presence_of_element_located(
                webdriver_test_ux, const.TIMEOUT_STEP_CIERRE_DE_SESION_INPUT_LOGIN_EMAIL,
                name=const.HTML_STEP_CERRAR_SESION_NAME_INPUT_LOGIN_EMAIL)

            HtmlActions.webdriver_wait_presence_of_element_located(
                webdriver_test_ux, const.TIMEOUT_STEP_CIERRE_DE_SESION_INPUT_LOGIN_PASSWORD,
                name=const.HTML_STEP_CERRAR_SESION_NAME_INPUT_LOGIN_PASSWORD)

            json_eval = UtilsEvaluaciones.establecer_output_status_step(
                json_eval, 5, 0, True, const.MSG_OUTPUT_CIERRE_SESION_EXITOSO)

        except ElementNotInteractableException as e:
            msg_output = const.MSG_OUTPUT_CIERRE_SESION_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 5, 0, False, msg_output)

        except NoSuchElementException as e:
            msg_output = const.MSG_OUTPUT_CIERRE_SESION_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 5, 0, False, msg_output)

        except TimeoutException as e:
            msg_output = const.MSG_OUTPUT_CIERRE_SESION_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 5, 0, False, msg_output)

        except ElementClickInterceptedException as e:
            msg_output = const.MSG_OUTPUT_CIERRE_SESION_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 5, 0, False, msg_output)

        json_eval = UtilsEvaluaciones.finalizar_tiempos_en_step(json_eval, 5, tiempo_step_inicio, fecha_inicio)

        return json_eval
