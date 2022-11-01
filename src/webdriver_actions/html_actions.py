from selenium.webdriver.common.by import By
from src.webdriver_actions import webdriver_actions_constantes
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class HtmlActions:

    @staticmethod
    def webdriver_wait_element_to_be_clickable(web_driver, time=5, id=None, xpath=None, link_text=None,
                                               partial_link_text=None, name=None, tag_name=None, class_name=None,
                                               css_selector=None):

        try:
            msg_exception = HtmlActions.generar_identificador_excepcion(id, xpath, link_text, partial_link_text,
                name, tag_name, class_name, css_selector)

            selector_por_buscar, elemento_html_por_localizar = HtmlActions.verificar_elemento_y_selector_por_localizar(
                id, xpath, link_text, partial_link_text, name, tag_name, class_name, css_selector)

            return WebDriverWait(web_driver, time).until(
                EC.element_to_be_clickable((selector_por_buscar, elemento_html_por_localizar)))

        except TimeoutException as e:
            e.msg = webdriver_actions_constantes.WEBDRIVER_WAIT_TIMEOUT_EXCEPTION.format(time, msg_exception, e.msg)
            raise e

    @staticmethod
    def webdriver_wait_presence_of_element_located(web_driver, time=5, id=None, xpath=None, link_text=None,
                                               partial_link_text=None, name=None, tag_name=None, class_name=None,
                                               css_selector=None):

        try:
            msg_exception = HtmlActions.generar_identificador_excepcion(id, xpath, link_text, partial_link_text,
                name, tag_name, class_name, css_selector)

            selector_por_buscar, elemento_html_por_localizar = HtmlActions.verificar_elemento_y_selector_por_localizar(
                id, xpath, link_text, partial_link_text, name, tag_name, class_name, css_selector)

            return WebDriverWait(web_driver, time).until(
                EC.presence_of_element_located((selector_por_buscar, elemento_html_por_localizar)))

        except TimeoutException as e:
            e.msg = webdriver_actions_constantes.WEBDRIVER_WAIT_TIMEOUT_EXCEPTION.format(time, msg_exception, e.msg)
            raise e

    @staticmethod
    def webdriver_wait_until_not_presence_of_element_located(web_driver, time=5, id=None, xpath=None, link_text=None,
                                               partial_link_text=None, name=None, tag_name=None, class_name=None,
                                               css_selector=None):

        try:
            msg_exception = HtmlActions.generar_identificador_excepcion(id, xpath, link_text, partial_link_text,
                name, tag_name, class_name, css_selector)

            selector_por_buscar, elemento_html_por_localizar = HtmlActions.verificar_elemento_y_selector_por_localizar(
                id, xpath, link_text, partial_link_text, name, tag_name, class_name, css_selector)

            return WebDriverWait(web_driver, time).until_not(
                EC.presence_of_element_located((selector_por_buscar, elemento_html_por_localizar)))

        except TimeoutException as e:
            e.msg = webdriver_actions_constantes.WEBDRIVER_WAIT_UNTIL_NOT_TIMEOUT_EXCEPTION.format\
                (time, msg_exception, e.msg)
            raise e


    @staticmethod
    def verificar_elemento_y_selector_por_localizar(id=None, xpath=None, link_text=None,
                                               partial_link_text=None, name=None, tag_name=None, class_name=None,
                                               css_selector=None):

        if id is not None:
            selector_por_buscar = By.ID
            elemento_html_por_localizar = id
        elif xpath is not None:
            selector_por_buscar = By.XPATH
            elemento_html_por_localizar = xpath
        elif link_text is not None:
            selector_por_buscar = By.LINK_TEXT
            elemento_html_por_localizar = link_text
        elif partial_link_text is not None:
            selector_por_buscar = By.PARTIAL_LINK_TEXT
            elemento_html_por_localizar = partial_link_text
        elif name is not None:
            selector_por_buscar = By.NAME
            elemento_html_por_localizar = name
        elif tag_name is not None:
            selector_por_buscar = By.TAG_NAME
            elemento_html_por_localizar = tag_name
        elif class_name is not None:
            selector_por_buscar = By.CLASS_NAME
            elemento_html_por_localizar = class_name
        elif css_selector is not None:
            selector_por_buscar = By.CSS_SELECTOR
            elemento_html_por_localizar = css_selector
        else:
            raise NoSuchElementException(msg='Sucedio un error NoSuchElementException. No se establecio el '
                                             'identificador o clase css del elemento HTML por buscar')

        return selector_por_buscar, elemento_html_por_localizar


    @staticmethod
    def enviar_data_keys(elementoHtml, dataKey: str, id=None, class_name=None, xpath=None, name=None):

            try:
                identifier_message = HtmlActions.generar_identificador_excepcion(id=id, class_name=class_name,
                                                                                 xpath=xpath, name=name)

                elementoHtml.send_keys(dataKey)

            except ElementNotInteractableException as e:
                e.msg = webdriver_actions_constantes.SEND_KEY_ElEMENT_NOT_INTERACTABLE_EXCEPTION.format(
                    identifier_message, e.msg)
                raise e

            except NoSuchElementException as e:
                e.msg = webdriver_actions_constantes.SEND_KEY_NO_SUCH_ELEMENT_EXCEPTION.format(identifier_message, e.msg)
                raise e

            except TimeoutException as e:
                e.msg = webdriver_actions_constantes.SEND_KEY_TIME_OUT_EXCEPTION.format(identifier_message, e.msg)
                raise e

            except ElementClickInterceptedException as e:
                e.msg = webdriver_actions_constantes.SEND_KEY_ELEMENT_CLICK_INTERCEPTED_EXCEPTION.format(
                    identifier_message, e.msg)
                raise e

            except StaleElementReferenceException as e:
                e.msg = webdriver_actions_constantes.SEND_KEY_STALE_ELEMENT_REFERENCE_EXCEPTION.format(
                    identifier_message, e.msg)
                raise e

            except WebDriverException as e:
                e.msg = webdriver_actions_constantes.SEND_KEY_WEBDRIVER_EXCEPTION.format(
                    identifier_message, e.msg)
                raise e


    @staticmethod
    def click_html_element(html_element, id=None, class_name=None, xpath=None, name=None):
        try:
            identifier_message = HtmlActions.generar_identificador_excepcion(id=id, class_name=class_name,
                                                                                      xpath=xpath, name=name)
            html_element.click()

        except ElementNotInteractableException as e:
            e.msg = webdriver_actions_constantes.CLICK_ElEMENT_NOT_INTERACTABLE_EXCEPTION.format(
                identifier_message, e.msg)
            raise e

        except NoSuchElementException as e:
            e.msg = webdriver_actions_constantes.CLICK_NO_SUCH_ELEMENT_EXCEPTION.format(identifier_message, e.msg)
            raise e

        except TimeoutException as e:
            e.msg = webdriver_actions_constantes.CLICK_TIME_OUT_EXCEPTION.format(identifier_message, e.msg)
            raise e

        except ElementClickInterceptedException as e:
            e.msg = webdriver_actions_constantes.CLICK_ELEMENT_CLICK_INTERCEPTED_EXCEPTION.format(
                identifier_message, e.msg)
            raise e

        except StaleElementReferenceException as e:
            e.msg = webdriver_actions_constantes.CLICK_STALE_ELEMENT_REFERENCE_EXCEPTION.format(
                identifier_message, e.msg)
            raise e

        except WebDriverException as e:
            e.msg = webdriver_actions_constantes.CLICK_WEBDRIVER_EXCEPTION.format(
                identifier_message, e.msg)
            raise e

    @staticmethod
    def generar_identificador_excepcion(id=None, xpath=None, link_text=None, partial_link_text=None,
                                        name=None, tag_name=None, class_name=None, css_selector=None):

        identifier_message = ''

        if id is not None:
            identifier_message = 'elemento con el id {}'.format(id)
        elif xpath is not None:
            identifier_message = 'elemento con el xpath {}'.format(xpath)
        elif link_text is not None:
            identifier_message = 'elemento con el link text {}'.format(class_name)
        elif partial_link_text is not None:
            identifier_message = 'elemento con el partial link text {}'.format(class_name)
        elif name is not None:
            identifier_message = 'elemento con el name {}'.format(name)
        elif tag_name is not None:
            identifier_message = 'elemento con el tag name {}'.format(class_name)
        elif class_name is not None:
            identifier_message = 'elemento con el class name {}'.format(class_name)
        elif css_selector is not None:
            identifier_message = 'elemento con el selector css {}'.format(class_name)

        return identifier_message
