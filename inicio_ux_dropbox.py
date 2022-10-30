import configparser
import json
import sys
import time
from os import path
from pathlib import Path
import src.validaciones_json.constantes_json as jsonConst
from src.step_evaluaciones.evaluaciones_drop_box import EvaluacionesDropBoxDriveSteps
from src.utils.utils_format import FormatUtils
from src.utils.utils_main import UtilsMain
from src.utils.utils_temporizador import Temporizador
from src.validaciones_json.json_evaluacion_base import GeneradorJsonBaseEvaluacion
from src.webdriver_config import config_constantes
from src.webdriver_config.config_webdriver import ConfiguracionWebDriver
from pyvirtualdisplay import Display


def verificacion_estatus_final(json_evaluacion):
    val_paso_1 = True if json_evaluacion["steps"][0]["status"] == jsonConst.SUCCESS else False
    val_paso_2 = True if json_evaluacion["steps"][1]["status"] == jsonConst.SUCCESS else False
    val_paso_3 = True if json_evaluacion["steps"][2]["status"] == jsonConst.SUCCESS else False
    val_paso_4 = True if json_evaluacion["steps"][3]["status"] == jsonConst.SUCCESS else False
    val_paso_5 = True if json_evaluacion["steps"][4]["status"] == jsonConst.SUCCESS else False
    val_paso_6 = True if json_evaluacion["steps"][5]["status"] == jsonConst.SUCCESS else False

    eval_final = val_paso_1 and val_paso_2 and val_paso_3 and \
        val_paso_4 and val_paso_5 and val_paso_6

    return jsonConst.SUCCESS if eval_final else jsonConst.FAILED


def verificacion_script_argumento_json(argumento_script_json):
    """
    :param argumento_script_json:
    :return:
    """
    if not FormatUtils.verificar_keys_json(argumento_script_json):
        return False

    elif not path.exists(argumento_script_json['pathImage']):
        print('La imagen/archivo por cargar dentro de la plataforma Claro Drive no fue localizado dentro del server, '
              'favor de verificar nuevamente el path de la imagen/archivo.')
        return False

    elif not path.isfile(argumento_script_json['pathImage']):
        print('El path de la imagen/archivo establecida, no corresponde a un archivo o imagen valida, favor de '
              'verificar nuevamente el path del archivo.')
        return False

    return True

def verificacion_archivo_config(archivo_config: configparser.ConfigParser):
    """
    Funcion el cual permite verificar que el archivo config.ini contenga todos los parametros necesarios. En caso
    de que contenga las secciones y keys establecidos, la funcion devolvera True, en caso contrario regresara False

    :return:
    """
    validacion_total = True

    bool_ruta = archivo_config.has_option('Driver', 'ruta')
    bool_using_webdriver = archivo_config.has_option(
        'Driver', 'using_webdriver')
    bool_folder_descargas = archivo_config.has_option(
        'Driver', 'folder_descargas')
    bool_headless = archivo_config.has_option('Driver', 'headless')

    if not bool_ruta:
        print('Favor de establecer el path del webdriver a utilizar dentro del archivo config.ini')
        validacion_total = False
    elif not bool_using_webdriver:
        print('Favor de establecer el tipo/nombre del webdriver a utilizar dentro del archivo config.ini')
        validacion_total = False
    elif not bool_folder_descargas:
        print('Favor de establecer el path en donde residiran las descargas dentro del archivo config.ini')
        validacion_total = False
    elif not bool_headless:
        print('Favor de establecer la opcion/configuracion headless dentro del archivo config.ini')
        validacion_total = False

    return validacion_total


def ejecucion_validaciones_drop_box(webdriver, argumento_script_json):

    nombre_de_imagen_sin_extension = Path(
        argumento_script_json['pathImage']).stem
    nombre_de_imagen_con_extension = path.basename(
        argumento_script_json['pathImage'])
    config_constantes.NOMBRE_IMAGEN_POR_CARGAR_CON_EXTENSION = path.basename(
        argumento_script_json['pathImage'])
    archivo_config = FormatUtils.lector_archivo_ini()
    url_login = archivo_config.get('Dropbox_config', 'url_login')

    # establece los datetime de inicio para la prueba UX
    tiempo_inicial_ejecucion_prueba = Temporizador.obtener_tiempo_timer()
    fecha_prueba_inicial = Temporizador.obtener_fecha_tiempo_actual()

    # se genera el json de evaluacion
    json_evaluacion_drop_box = GeneradorJsonBaseEvaluacion.generar_nuevo_template_json()
    evaluaciones_steps_drop_box = EvaluacionesDropBoxDriveSteps()

    json_evaluacion_drop_box = evaluaciones_steps_drop_box.ingreso_pagina_principal_dropbox(
        webdriver, json_evaluacion_drop_box, url_login)

    json_evaluacion_drop_box = evaluaciones_steps_drop_box.inicio_sesion_dropbox(
        webdriver, json_evaluacion_drop_box, argumento_script_json, url_login)

    json_evaluacion_drop_box = evaluaciones_steps_drop_box.cargar_archivo_dropbox(
        webdriver, json_evaluacion_drop_box, argumento_script_json, nombre_de_imagen_sin_extension,
        nombre_de_imagen_con_extension)

    json_evaluacion_drop_box = evaluaciones_steps_drop_box.descargar_archivo_dropbox(
        webdriver, json_evaluacion_drop_box, nombre_de_imagen_con_extension)

    json_evaluacion_drop_box = evaluaciones_steps_drop_box.eliminar_archivo_dropbox(
        webdriver, json_evaluacion_drop_box, nombre_de_imagen_con_extension)

    json_evaluacion_drop_box = evaluaciones_steps_drop_box.cerrar_sesion_dropbox(
        webdriver, json_evaluacion_drop_box)

    tiempo_final_ejecucion_prueba = Temporizador.obtener_tiempo_timer() - \
        tiempo_inicial_ejecucion_prueba
    fecha_prueba_final = Temporizador.obtener_fecha_tiempo_actual()

    json_evaluacion_drop_box['start'] = fecha_prueba_inicial
    json_evaluacion_drop_box['end'] = fecha_prueba_final
    json_evaluacion_drop_box['time'] = tiempo_final_ejecucion_prueba
    json_evaluacion_drop_box['status'] = verificacion_estatus_final(
        json_evaluacion_drop_box)

    json_padre = {}
    json_padre.update({'body': json_evaluacion_drop_box})

    time.sleep(2)

    webdriver.close()
    webdriver.quit()

    return json_padre


def main():

    # verificacion del archivo de configuracion (config.ini)
    archivo_config = FormatUtils.lector_archivo_ini()

    if not verificacion_archivo_config(archivo_config):
        sys.exit()

    # valida si se ejecutara con xvbf
    running_in_xbbf_mode = archivo_config.getboolean(
        'Driver', 'running_with_xvbf')
    display = None

    if running_in_xbbf_mode:
        display = Display(size=(1920, 1080))
        display.start()

    param_archivo_config_path_web_driver = archivo_config.get('Driver', 'ruta')
    param_archivo_config_directorio_descargas = archivo_config.get(
        'Driver', 'folder_descargas')
    param_archivo_config_using_webdriver = archivo_config.getboolean(
        'Driver', 'using_webdriver')

    argumento_script_json = {
        'pathImage': archivo_config.get('path_and_credentials', 'path_descargas'),
        'user': archivo_config.get('path_and_credentials', 'usuario'),
        'password': archivo_config.get('path_and_credentials', 'password')}

    # # verifica el formato del argumento JSON y obtiene cada uno de los parametros
    if not verificacion_script_argumento_json(argumento_script_json):
        sys.exit()

    # establece la carpeta de descarga dinamica (donde se descargara la imagen desde el portal de claro drive)
    config_constantes.PATH_CARPETA_DESCARGA = UtilsMain.generar_carpeta_descarga_dinamica(
        argumento_script_json['pathImage'])

    UtilsMain.crear_directorio(config_constantes.PATH_CARPETA_DESCARGA)

    # se establece la configuracion del webdriver
    webdriver_config = ConfiguracionWebDriver(param_archivo_config_path_web_driver,
                                              param_archivo_config_directorio_descargas,
                                              param_archivo_config_using_webdriver)

    # se establece y obtiene el webdriver/navegar para la ejecucion de las pruebas UX en claro drive
    webdriver_ux_test = webdriver_config.configurar_obtencion_web_driver()

    webdriver_ux_test.set_window_position(0, 0)
    webdriver_ux_test.maximize_window()

    # ejecuta cada uno de los pasos de la UX en Drop Box
    resultado_json_evaluacines_ux_drop_box = ejecucion_validaciones_drop_box(
        webdriver_ux_test, argumento_script_json)

    if running_in_xbbf_mode:
        display.stop()

    UtilsMain.eliminar_directorio_con_contenido(
        config_constantes.PATH_CARPETA_DESCARGA)

    print(json.dumps(resultado_json_evaluacines_ux_drop_box))


if __name__ == '__main__':
    main()
