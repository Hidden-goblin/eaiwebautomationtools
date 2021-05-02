# -*- coding: utf-8 -*-
import logging
from time import sleep

from selenium.webdriver.remote.webelement import WebElement

from .finders import find_element, find_from_elements
from .information import is_field_exist, is_field_displayed
from .drivers_tools import driver_field_validation, web_element_validation
from selenium.common.exceptions import InvalidElementStateException, NoSuchElementException, \
    StaleElementReferenceException
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

log = logging.getLogger(__name__)


def fill_elements(driver=None, fields=None, web_element=None, data=None):
    """
    Fill a field set with data where the field and data are identified by the same key
    Keys are taken from the data set dictionary
    :param driver: a selenium web driver
    :param fields: a dictionary of fields
    :param web_element: a web_element to search elements from
    :param data: a dictionary of data
    :raise AssertionError: driver is not define, fields and data doesn't have the same keys
    :raise InvalidElementStateException: rethrown from fill_element
    :raise Exception: all other issues
    :return: 0 if success
    """
    try:
        if any(key not in fields.keys() for key in data.keys()):
            log.error(f"Missing fields for the given data. "
                      f"Data keys '{data.keys()}'. "
                      f"Fields keys '{fields.keys()}'")
            raise KeyError("Data keys are not included in Fields keys")

        for key in data:
            fill_element(driver=driver, field=fields[key], web_element=web_element, value=data[key])
        return 0
    except InvalidElementStateException as invalid_element:
        log.error(invalid_element)
        raise InvalidElementStateException(f"Element '{fields[key]}' must be user-editable") from None
    except NoSuchElementException:
        log.error(f"Field '{fields[key]}' could not be found for filling")
        raise NoSuchElementException(f"Field '{fields[key]}' could not be found for filling") from None


def fill_element(driver=None, field=None, web_element=None, value=None):
    """
    Fill the given field with the value.
    :param web_element:
    :param driver: a selenium web driver
    :param field: a dictionary
    :param value: a string or castable to string
    :raise AttributeError: web driver is not set or field is not a dictionary
    :raise ValueError: field doesn't contains the expected field
    :raise InvalidElementStateException: if the element is not user-editable
    :raise NoSuchElementException: element to be filled cannot be found
    :return: 0 if success
    """
    try:
        driver_field_validation(driver, field, log)
        iteration = 0
        while iteration < 5:
            try:
                elem = find_element(driver=driver, field=field, web_element=web_element)
                if value:
                    elem.clear()
                    elem.send_keys(str(value))
                else:
                    number_of_backspace_hit = len(elem.get_attribute('value'))
                    elem.send_keys(number_of_backspace_hit * Keys.BACKSPACE)
                return 0
            except StaleElementReferenceException:
                log.info("StaleElementReferenceException retry after 100ms sleep")
                iteration += 1
                sleep(0.1)
    except InvalidElementStateException as invalid_element:
        log.error(invalid_element)
        raise InvalidElementStateException(f"Element '{field}' must be user-editable") from None
    except NoSuchElementException:
        log.error(f"Field '{field}' could not be found for filling")
        raise NoSuchElementException(f"Field '{field}' could not be found for filling") from None


def select_in_dropdown(driver=None, field=None, visible_text=None, value=None):
    """
    see https://stackoverflow.com/questions/7867537/selenium-python-drop-down-menu-option-value
    see https://sqa.stackexchange.com/questions/1355/what-is-the-correct-way-to-select-an-option-using-seleniums-python-webdriver # noqa
    see https://seleniumhq.github.io/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.select.html # noqa
    :raise AssertionError: driver is not define, field is not valid
    :return:
    """
    driver_field_validation(driver, field, log)

    try:
        iteration = 0
        while iteration < 5:
            try:
                my_select = Select(find_element(driver=driver, field=field))

                if visible_text is not None:
                    my_select.select_by_visible_text(visible_text)
                elif value is not None:
                    my_select.select_by_value(value)
                else:
                    raise Exception("select_in_dropdown can't select with no value.")

                return 0
            except StaleElementReferenceException:
                log.info("StaleElementReferenceException retry after 100ms sleep")
                iteration += 1
                sleep(0.1)
    except NoSuchElementException as no_such_element:
        log.error(no_such_element.args)
        raise NoSuchElementException(no_such_element.args[0]) from None
    except Exception as exception:
        log.error(exception.args)
        raise Exception(exception.args[0]) from None


def select_in_angular_dropdown(driver=None, root_field=None, visible_text: str = None):
    """
    Select a field within a mat_option list

    If root_field is defined then click it and search for visible_text in mat-option elements.
    Otherwise only search for visible_text in mat-options elements
    :param visible_text: a string to search
    :param driver: a selenium web driver
    :param root_field: a dictionary for the container
    :return:
    """
    try:
        if root_field is not None:
            click_element(driver=driver, field=root_field)
            sleep(0.1)

        if is_field_exist(driver=driver, field={"type": "tag_name", "value": "mat-option"}):
            element = find_from_elements(driver=driver,
                                         field={"type": "tag_name", "value": "mat-option"},
                                         text=visible_text)
            element.click()
        else:
            raise Exception('No options displayed within 5 seconds')

    except StaleElementReferenceException as stale_exception:
        log.warning("StaleElementReferenceException. Selection should be done.\n{}".format(
            stale_exception.args))
        return 0
    except Exception as exception:
        log.error(exception.args)
        raise Exception(exception.args[0]) from None


def click_element(driver=None, field=None, web_element: WebElement = None):
    """
    Do simple left click on the given field or on the sub element when web_element is provided
    :param driver: a selenium web driver
    :param field: a dictionary
    :param web_element: an element from which to find the element to click
    :raise AssertionError: driver is not define, field is not valid
    :return: 0 if success
    """
    driver_field_validation(driver, field, log)
    web_element_validation(web_element, log)
    iteration = 0
    while iteration < 5:
        try:
            web_element = find_element(driver=driver, field=field, web_element=web_element)
            web_element.click()
            return 0
        except StaleElementReferenceException:
            log.info("StaleElementReferenceException retry after 100ms sleep")
            iteration += 1
            sleep(0.1)


def set_checkbox(driver=None, field=None, is_checked=None):
    """
    Set a checkbox to a specific state: True for checked, False for unchecked
    :param driver: a selenium web driver
    :param field: a field identifier as a dictionary
    :param is_checked: the field check value as a boolean (True/False)
    :raise AttributeError: driver is not define, field is not valid, is_checked is not a boolean
    :raise ValueError: field dictionary doesn't contain the minimal keys
    :return: 0 if success
    """
    driver_field_validation(driver, field, log)
    if not isinstance(is_checked, bool):
        log.error(f"is_checked is expected to be a boolean. Get {type(is_checked)}")
        raise TypeError("is_checked is expected to be a boolean.")

    elem = find_element(driver=driver, field=field)
    current_state = bool(elem.get_attribute("checked"))
    if current_state is not is_checked:
        elem.click()

    # Check if the element has been set in the expected status
    current_state = bool(elem.get_attribute("checked"))
    if current_state is not is_checked:
        log.error(f"The element '{field}' can't be set to the expected status '{is_checked}'.")
        raise Exception(
            f"The element '{field}' can't be set to the expected status '{is_checked}'.")
    return 0


def hover_element(driver=None, field=None):
    """
    Do simple hover on the given field
    :param driver: a selenium web driver
    :param field: a dictionary
    :raise AssertionError: driver is not define, field is not valid
    :return: 0 if success
    """
    driver_field_validation(driver, field, log)
    try:
        elem = find_element(driver=driver, field=field)
        hover = ActionChains(driver).move_to_element(elem)
        hover.perform()
        return 0
    except Exception as exception:
        logging.error(exception.args)
        raise Exception(exception.args[0]) from None


def select_in_elements(driver=None, field=None, displayed_text=None):
    """
    TODO Add the capability to select a field from an webelement child
    Do a click on the element which text
    :param driver: a selenium web driver
    :param field: a dictionary
    :param displayed_text: a string
    :return: 0 if success
    """
    driver_field_validation(driver, field, log)
    if displayed_text is None or not isinstance(displayed_text, str):
        raise AttributeError("Displayed text must be a non-empty string")
    try:
        if is_field_displayed(driver=driver, field=field):
            element = find_from_elements(driver=driver, field=field, text=displayed_text)
            element.click()
        return 0
    except Exception as exception:
        logging.error(exception.args)
        raise Exception(exception.args[0]) from None
