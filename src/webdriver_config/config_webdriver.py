import sys
from selenium import webdriver
import src.webdriver_config.config_constantes as config_constantes
from src.utils.utils_format import FormatUtils
from src.utils.utils_main import UtilsMain
import undetected_chromedriver.v2 as UC


class ConfiguracionWebDriver:

    def __init__(self, ruta_web_driver, folder_de_descargas, using_webdriver):

        self.ruta_web_driver = ruta_web_driver
        self.folder_de_descargas = folder_de_descargas
        self.using_webdriver = using_webdriver

    def inicializar_webdriver(self):
        archivo_config_ini = FormatUtils.lector_archivo_ini()
        modo_headless = archivo_config_ini.getboolean('Driver', 'headless')
        mandar_log_a_dev_null = archivo_config_ini.getboolean('Driver', 'log_path_dev_null')

        # opciones_chrome = webdriver.ChromeOptions()
        opciones_chrome = UC.ChromeOptions()

        # ignora las certificaciones de seguridad, esto solamente se realiza para la experiencia de usuario
        opciones_chrome.add_argument('--ignore-certificate-errors')
        opciones_chrome.add_argument('--allow-running-insecure-content')
        opciones_chrome.add_argument("--enable-javascript")
        opciones_chrome.add_argument('window-size=1920x1080')
        opciones_chrome.add_argument('--no-sandbox')
        opciones_chrome.add_argument('--enable-sync')

        # establece el modo headless, esto dependiendo de la opcion que se tenga en el archivo config.ini
        if modo_headless:
            opciones_chrome.add_argument("--headless")

        opciones_chrome.add_experimental_option('excludeSwitches', ['enable-logging'])
        opciones_chrome.add_experimental_option('prefs', {'download.default_directory':
            config_constantes.PATH_CARPETA_DESCARGA})

        prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": config_constantes.PATH_CARPETA_DESCARGA,
                 "directory_upgrade": True}

        opciones_chrome.add_experimental_option("prefs", prefs)

        chrome_capabilities = webdriver.DesiredCapabilities().CHROME.copy()
        chrome_capabilities['acceptSslCerts'] = True
        chrome_capabilities['acceptInsecureCerts'] = True

        # establece el directorio al cual se redireccionara el log generado por el chromedriver
        if mandar_log_a_dev_null:
            param_service_log_path = config_constantes.DEV_NULL
        else:
            param_service_log_path = None

        try:
            webdriver_chrome = UC.Chrome(driver_executable_path=self.ruta_web_driver,
                                         chrome_options=opciones_chrome,
                                         desired_capabilities=chrome_capabilities,
                                         service_log_path=param_service_log_path,
                                         headless=modo_headless)

            # establece algunos parametros para la descarga en la carpeta de descargas
            params = {
                "behavior": "allow",
                "downloadPath": config_constantes.PATH_CARPETA_DESCARGA
            }
            webdriver_chrome.execute_cdp_cmd("Page.setDownloadBehavior", params)

        except FileNotFoundError as e:
            print('Sucedio un error al intentar configurar el webdriver: {}'.format(e))
            sys.exit()

        except Exception as e:
            print('Sucedio una excepcion al intentar configurar el webdriver {}'.format(e))
            sys.exit()

        return webdriver_chrome

    def configurar_obtencion_web_driver(self):
        if self.using_webdriver:
            # verifica que el parametro del directorio del webdriver se encuentre establecido y sea un directorio valido
            if len(self.ruta_web_driver.strip()) == 0 and not UtilsMain.verificar_path_es_directorio(
                    self.ruta_web_driver.strip()):
                print(config_constantes.MSG_ERROR_PROP_INI_WEBDRIVER_SIN_CONFIGURAR)
                sys.exit()
        else:
            self.ruta_web_driver = None

        # verifica que el parametro del directorio de descargas se encuentre establecido y sea un directorio valido
        if not UtilsMain.verificar_path_es_directorio(self.folder_de_descargas):
            print(config_constantes.MSG_ERROR_PROP_INI_FOLDER_DESCARGAS_SIN_CONFIGURAR)
            sys.exit()

        driver_configurado = self.inicializar_webdriver()

        return driver_configurado
