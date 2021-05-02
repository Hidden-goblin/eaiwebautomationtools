# -*- coding: utf-8 -*-
from logging import getLogger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .drivers_tools import driver_field_validation, web_drivers_tuple
from .finders import find_element


log = getLogger(__name__)


def is_field_exist(driver=None, field=None, until=5):
    """
    Test if the field given as a {"type":"id","value":"toto"} dictionary exists.
    :param driver: a selenium web driver
    :param field: a dictionary
    :param until: an int as the wait time
    :raise TypeError: driver isn't of the expected type
    :return: a web element if exist, None otherwise
    """
    try:
        driver_field_validation(driver, field, log)

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

    except TimeoutException:
        log.warning(f"information.is_field_exist raised a TimeoutException for "
                    f"the following field '{field}'")
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
    driver_field_validation(driver, field, log)
    element = is_field_exist(driver=driver, field=field)
    return (element.text is not None and text in element.text) or (
            element.get_attribute("value") is not None
            and text in element.get_attribute("value"))


def is_alert_present(driver=None, until=5):
    """
    Tells if whatever an alert is present or not.
    :param driver: a selenium web driver
    :param until: time to wait.
    :return: True or False.
    """
    try:
        driver_field_validation(driver, {"type": "id", "value": "fake"}, log)
        if WebDriverWait(driver, until).until(EC.alert_is_present()):
            return True
    except TimeoutException:
        return False


def element_text(driver=None, field=None, web_element=None):
    """
    Return the text of the element
    :param driver: a selenium web driver
    :param field: a dictionary corresponding to the field to retrieve the text
    :param web_element: a webElement to search the field from
    :raise TypeError: from finders.find_element method
    :raise ValueError: from finders.find_element method
    :raise Exception: if text and value are defined but not identical
    :return: the element text or value, empty if no text or value
    """
    element = find_element(driver=driver, field=field, web_element=web_element)
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
    driver_field_validation(driver, {"type": "id", "value": "fake"}, log)
    return len(driver.window_handles)


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
    if element is not None:
        if attribute is not None:
            return element.get_attribute(attribute)
        else:
            return element.is_enabled()
    else:
        return False


def where_am_i(driver=None):
    """
    Return the current location URL
    :param driver: a selenium web driver
    :return: String. The current URL
    """
    if driver is None or not isinstance(driver, web_drivers_tuple()):
        raise TypeError("Driver is expected as a WebDriver")

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


def retrieve_tabular(driver=None, field=None, row_and_col=("tr", "td", "th")) -> list:
    """
    Return the tabular as a list of elements.
    Elements are either lists or dictionaries depending on the presence of headers
    :param driver: a selenium web driver
    :param row_and_col: a tuple of row and col tags plus header tag. Defaulted to ('tr', 'td', 'th').
     Please mind the order. ROW, COL, COL HEADER
    :param field: a dictionary
    :return: list
    """
    tabular = find_element(driver, field)
    rows = tabular.find_elements_by_tag_name(row_and_col[0])
    tabular_as_list = list()

    for row in rows:
        columns = row.find_elements_by_tag_name(row_and_col[1])
        if not columns:
            columns = row.find_elements_by_tag_name(row_and_col[2])
        tabular_as_list.append([column.text for column in columns])

    return tabular_as_list
