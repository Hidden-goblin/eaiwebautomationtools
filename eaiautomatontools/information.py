# -*- coding: utf-8 -*-
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .drivers_tools import web_drivers_tuple
from .finders import find_element


def is_field_exist(driver=None, field=None, until=5):
    """
    Test if the field given as a {"type":"id","value":"toto"} dictionary exists.
    :param driver: a selenium web driver
    :param field: a dictionary
    :param until: an int as the wait time
    :raise AssertionError: driver isn't of the expected type
    :return: a web element if exist, None otherwise
    """
    try:
        assert driver is not None and isinstance(driver, web_drivers_tuple()),\
            "Driver is expected."
        switcher = {
            "id": By.ID,
            "name": By.NAME,
            "class_name": By.CLASS_NAME,
            "css": By.CSS_SELECTOR,
            "link_text": By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT,
            "tag_name": By.TAG_NAME,
            "xpath": By.XPATH
        }

        return WebDriverWait(driver, until).until(
            EC.presence_of_element_located((switcher[field["type"]], field["value"])))
    except AssertionError as assertion:
        logging.error("information.is_field_exist raised an assertion with following"
                      " input driver:'{}', field:'{}' and until:'{}'. "
                      "Assertion is '{}'".format(driver, field, until, assertion.args))
        raise
    except TimeoutException:
        logging.warning("""information.is_field_exist raised a TimeoutException for
         the following field '{}' """.format(field))
        return None


def is_field_contains_text(driver=None, field=None, text=None):
    """
    Check if the given field contains the text either as a DOM text or value text.
    {"type":"id","value":"toto"}
    :param driver: a selenium web driver
    :param field: a dictionary
    :param text: a string for the text to be in the field
    :raise AssertionError: driver isn't of the expected type
    :return: True if the field contains the text, False otherwise
    """
    try:
        assert driver is not None and isinstance(driver, web_drivers_tuple()),\
            "Driver is expected."
        element = is_field_exist(driver=driver, field=field)
        if (element.text is not None and text in element.text) or (
                element.get_attribute("value") is not None
                and text in element.get_attribute("value")):
            return True
        else:
            return False
    except AssertionError as assertion:
        logging.error("information.is_field_exist raised an assertion with "
                      "following input driver:'{}', field:'{}' and text:'{}'. "
                      "Assertion is '{}'".format(driver, field, text, assertion.args))
        raise


def is_alert_present(driver=None, until=5):
    """
    Tells if whatever an alert is present or not.
    :param driver: a selenium web driver
    :param until: time to wait.
    :return: True or False.
    """
    try:
        assert driver is not None and isinstance(driver, web_drivers_tuple()), "Driver is expected."
        if WebDriverWait(driver, until).until(EC.alert_is_present()):
            return True
    except AssertionError as assertion:
        logging.error("information.is_alert-present raised an assertion with "
                      "following input driver:'{}' and until:'{}'. "
                      "Assertion is '{}'".format(driver, until, assertion.args))
        raise
    except TimeoutException:
        return False


def element_text(driver=None, field=None):
    """
    Return the text of the element
    :param driver: a selenium web driver
    :param field: a dictionary
    :raise AssertionError: from eaifinders.find_element method
    :raise Exception: if text and value are defined but not identical
    :return: the element text or value, empty if no text or value
    """
    element = find_element(driver=driver, field=field)
    element_text_ = element.text
    element_value = element.get_attribute("value")

    if element_text_ and not element_value:
        return element_text_
    elif not element_text_ and element_value:
        return element_value
    elif element_text_ is not None and element_value is not None \
            and element_text_ in element_value and element_value in element_text_:
        return element_text_
    elif element_text_ is not None and element_value is not None and (
            element_text_ not in element_value or element_value not in element_text_):
        raise Exception("Can't serve the element 'text' having both data for text and"
                        " attribute value")
    else:
        return ""


def how_many_windows(driver=None):
    """
    Return the number of windows at the method execution.
    :param driver: a selenium web driver
    :return: the number of windows
    """
    try:
        assert driver is not None and isinstance(driver, web_drivers_tuple()),\
            "Driver is expected."
        return len(driver.window_handles)
    except AssertionError as assertion:
        logging.error("information.is_alert-present raised an assertion with "
                      "following input driver:'{}'. "
                      "Assertion is '{}'".format(driver, assertion.args))
        raise


def is_field_displayed(driver=None, field=None):
    """
    Check if the element is displayed. You may not interact with it.
    :param driver: a selenium web driver
    :param field: a dictionary
    :return: Boolean. True if element is displayed, false otherwise.
    """
    element = is_field_exist(driver=driver, field=field)
    if element is not None:
        return element.is_displayed()
    else:
        return False


def is_field_enabled(driver=None, field=None, attribute=None):
    """
    Check if the element is enabled.
    :param attribute: the attribute to check for enabled
    :param driver: a selenium web driver
    :param field: a dictionary
    :return: Boolean. True if element is enabled, false otherwise for non attribute.
            Attribute string otherwise
    """
    element = is_field_exist(driver=driver, field=field)
    if attribute is None:
        if element is not None:
            return element.is_enabled()
        else:
            return False
    else:
        if element is not None:
            return element.get_attribute(attribute)
        else:
            return False


def where_am_i(driver=None):
    """
    Return the current location URL
    :param driver: a selenium web driver
    :return: String. The current URL
    """
    return driver.current_url


def is_checkbox_checked(driver=None, field=None, is_angular=False):
    """
    Return the checkbox status
    :param driver: a selenium web driver
    :param field: a dictionary
    :param is_angular: boolean
    :return: boolean
    """
    element = is_field_exist(driver=driver, field=field)

    if is_angular:
        return bool(element.get_attribute("ng-reflect-checked"))
    else:
        return bool(element.get_attribute("checked"))


def retrieve_tabular(driver=None, field=None) -> list:
    """
    Return the tabular as a list of elements.
    Elements are either lists or dictionaries depending on the presence of headers
    :param driver: a selenium web driver
    :param field: a dictionary
    :return: list
    """
    pass
