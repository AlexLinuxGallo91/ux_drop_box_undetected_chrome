import configparser
import os
import json


class FormatUtils:

    @staticmethod
    def cadena_a_json_valido(cadena=''):
        try:
            obj_json = json.loads(cadena)
            return True
        except ValueError as e:
            print('El texto "{}" no es un objeto JSON valido: {}, se omite experiencia de usuario Drop Box'.format(
                cadena, e))
            return False

    @staticmethod
    def truncar_float_cadena(cifra_decimal):
        num = cifra_decimal

        if isinstance(cifra_decimal, str):
            try:
                num = float(cifra_decimal)
            except ValueError as e:
                num = 0

        num = round(num, 12)
        num = '{:.12f}'.format(num)
        return num

    @staticmethod
    def lector_archivo_ini():
        config = None

        try:
            config = configparser.ConfigParser()
            dir_module = os.path.dirname(__file__)
            dir_module = os.path.join(dir_module, '..', '..', 'config.ini')
            config.read(dir_module)
        except configparser.Error as e:
            print('sucedio un error al leer el archivo de configuracion: {}'.format(e))

        return config

    @staticmethod
    def verificar_keys_json(json):
        list_keys = ['user', 'password', 'pathImage']

        for key in list_keys:
            if key not in json:
                print('Favor de verificar el parametro json, la llave {} no esta presente dentro del json'.format(key))
                return False

        return True

    @staticmethod
    def establecer_path_de_descarga(path_folder_de_descarga, path_archivo_de_configuracion):

        if os.path.exists(path_archivo_de_configuracion):
            f = open(path_archivo_de_configuracion, 'r')
            r = f.read()
            f.close()

            obj_json = json.loads(r)
            obj_json['download']['default_directory'] = path_folder_de_descarga
            obj_json['download']['directory_upgrade'] = True

            # obj_json['savefile']['directory_upgrade'] = True
            obj_json['savefile'] = {}
            obj_json['savefile']['directory_upgrade'] = True

            f = open(path_archivo_de_configuracion, '+r')
            f.truncate()
            f.write(json.dumps(obj_json))
            f.close()








