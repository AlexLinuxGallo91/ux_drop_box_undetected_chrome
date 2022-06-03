from selenium.common.exceptions import TimeoutException

import src.validaciones_json.constantes_json as constantes_json
from src.utils.utils_format import FormatUtils
from src.utils.utils_main import UtilsMain
from src.utils.utils_temporizador import Temporizador
from src.webdriver_config import config_constantes


class UtilsEvaluaciones:

    @staticmethod
    def finalizar_tiempos_en_step(jsonEval, indice: int, tiempo_step_inicio, fecha_inicio):

        if tiempo_step_inicio is None:
            tiempo_step_inicio = Temporizador.obtener_tiempo_timer()

        tiempo_step_final = Temporizador.obtener_tiempo_timer() - tiempo_step_inicio
        fecha_fin = Temporizador.obtener_fecha_tiempo_actual()
        jsonEval["steps"][indice]["time"] = FormatUtils.truncar_float_cadena(tiempo_step_final)
        jsonEval["steps"][indice]["start"] = fecha_inicio
        jsonEval["steps"][indice]["end"] = fecha_fin

        return jsonEval

    @staticmethod
    def establecer_output_status_step(jsonEval, indice: int, sub_indice: int, paso_exitoso: bool, mensaje_output: str):

        status_del_step = constantes_json.SUCCESS if paso_exitoso else constantes_json.FAILED

        jsonEval["steps"][indice]["output"][sub_indice]["status"] = status_del_step
        jsonEval["steps"][indice]["status"] = status_del_step
        jsonEval["steps"][indice]["output"][sub_indice]["output"] = mensaje_output

        return jsonEval

    @staticmethod
    def generar_json_inicio_de_sesion_incorrecta(json_eval, tiempo_step_inicio, fecha_inicio, indice: int,
                                                 msg_output: str):

        if tiempo_step_inicio is None:
            tiempo_step_inicio = Temporizador.obtener_tiempo_timer()

        json_eval["steps"][indice]["output"][0]["status"] = constantes_json.FAILED
        json_eval["steps"][indice]["status"] = constantes_json.FAILED
        json_eval["steps"][indice]["output"][0]["output"] = msg_output

        tiempo_step_final = Temporizador.obtener_tiempo_timer() - tiempo_step_inicio
        fecha_fin = Temporizador.obtener_fecha_tiempo_actual()

        json_eval["steps"][indice]["time"] = FormatUtils.truncar_float_cadena(tiempo_step_final)
        json_eval["steps"][indice]["start"] = fecha_inicio
        json_eval["steps"][indice]["end"] = fecha_fin

        return json_eval

    @staticmethod
    def se_ingreso_correctamente_a_la_sesion(jsonEval):
        return True if jsonEval["steps"][1]["status"] == constantes_json.SUCCESS else False

    @staticmethod
    def se_ingreso_correctamente_a_la_pagina_principal(json_eval):
        return True if json_eval["steps"][0]["status"] == constantes_json.SUCCESS else False

    @staticmethod
    def se_cargo_correctamente_el_fichero(json_eval):
        return True if json_eval["steps"][2]["status"] == constantes_json.SUCCESS else False

    @staticmethod
    def verificar_descarga_en_ejecucion(nombre_del_archivo, extension_del_archivo, tiempo_de_espera=180):
        tiempo_inicio = Temporizador.obtener_tiempo_timer()
        se_descargo_el_archivo_exitosamente = False
        archivo_a_localizar = '{}{}'.format(nombre_del_archivo, extension_del_archivo)

        while (Temporizador.obtener_tiempo_timer() - tiempo_inicio) < tiempo_de_espera:
            lista_archivos = UtilsMain.obtener_lista_ficheros_en_directorio(config_constantes.PATH_CARPETA_DESCARGA)

            if archivo_a_localizar in lista_archivos:
                se_descargo_el_archivo_exitosamente = True
                break

        if not se_descargo_el_archivo_exitosamente:
            raise TimeoutException(msg='Han transcurrido 3 minutos sin finalizar la descarga del archivo {} desde '
                                       'el portal Claro Drive'.format(archivo_a_localizar))
