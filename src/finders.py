# -*- coding: utf-8 -*-
import logging
from .drivers_tools import web_drivers_tuple
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains

log = logging.getLogger(__name__)


def find_element(driver=None, field=None):
    """
    Look up for the field described as a dictionary {"type": string, "value":}.
    Example: {"type": "id", "value": "frmCentreNumber"}
    Optionally, you can specify a text an call the find_from_elements method
    :param driver: a selenium web driver
    :param field: a dictionary
    :raise AssertionError: if driver is not a proper web driver instance or
            the field is not a dictionary
    :raise KeyError: If the field variable doesn't contain the expected keys i.e. type and value
    :raise NoSuchElementException: If the field doesn't exist
    :return: a selenium web element
    """
    try:
        assert driver is not None and isinstance(driver, web_drivers_tuple()),\
            "Driver is expected."
        assert isinstance(field, dict), "Field must be a dictionary"
        if "type" not in field.keys() or "value" not in field.keys():
            raise KeyError("The field argument doesn't contains either the 'type' or 'value' key.")
        if "text" in field.keys():
            return find_from_elements(driver=driver, field=field, text=field['text'])
        # Define the association between a type and a selenium find action
        switcher = {
            "id": driver.find_element_by_id,
            "name": driver.find_element_by_name,
            "class_name": driver.find_element_by_class_name,
            "css": driver.find_element_by_css_selector,
            "link_text": driver.find_element_by_link_text,
            "partial_link_text": driver.find_element_by_partial_link_text,
            "tag_name": driver.find_element_by_tag_name,
            "xpath": driver.find_element_by_xpath
        }
        element = switcher[field["type"]](field["value"])
        actions = ActionChains(driver)
        actions.move_to_element(element)
        actions.perform()
        return element
    except AssertionError as assertion:
        log.error("finders.find_element raised an assertion with following input"
                  " driver:'{}' and field:'{}'. Assertion is '{}'".format(driver,
                                                                          field,
                                                                          assertion.args))
        raise
    except KeyError as key_error:
        log.error("In find_element didn't find the method for"
                  " '{}' finder method".format(field["type"]))
        raise KeyError(key_error)
    except NoSuchElementException as no_such_element:
        log.error("In find_element didn't find the element '{}'."
                  " Exception is '{}'".format(field, no_such_element.args))
        raise NoSuchElementException("Element designed by field '{}'"
                                     " could not be located.".format(field)) from None


def find_elements(driver=None, field=None):
    """
    Look up for the field described as a dictionary {"type": string, "value":}.
    Example: {"type": "id", "value": "frmCentreNumber"}
    :param driver: a selenium web driver
    :param field: a dictionary
    :raise AssertionError: if driver is not a proper web driver instance or
            the field is not a dictionary
    :raise KeyError: If the field variable doesn't contain the expected keys i.e. type and value
    :return: a list of selenium web element
    """
    try:
        assert driver is not None and isinstance(driver, web_drivers_tuple()),\
            "Driver is expected."
        assert isinstance(field, dict), "Field must be a dictionary"
        if "type" not in field.keys() or "value" not in field.keys():
            raise KeyError("The field argument doesn't contains either the 'type' or 'value' key.")
        # Define the association between a type and a selenium find action
        switcher = {
            "id": driver.find_elements_by_id,
            "name": driver.find_elements_by_name,
            "class_name": driver.find_elements_by_class_name,
            "css": driver.find_elements_by_css_selector,
            "link_text": driver.find_elements_by_link_text,
            "partial_link_text": driver.find_elements_by_partial_link_text,
            "tag_name": driver.find_elements_by_tag_name,
            "xpath": driver.find_elements_by_xpath
        }
        return switcher[field["type"]](field["value"])
    except AssertionError as assertion:
        log.error("finders.find_elements raised an assertion with following input"
                  " driver:'{}', field:'{}'. Assertion is '{}'".format(driver, field,
                                                                       assertion.args))
        raise
    except KeyError as key_error:
        log.error(
            "In find_elements didn't find the method for '{}' finder method".format(field["type"]))
        raise KeyError(key_error)


def find_from_elements(driver=None, field=None, text=None):
    """
    Try to locate an element using his text
    :param driver: a selenium web driver
    :param field: a dictionary
    :param text: a string
    :raise AssertionError: from the eaifinders.find_elements method
    :raise KeyError: from the eaifinders.find_elements method
    :raise NoSuchElementException: when no element is found
    :return: a selenium web element
    """
    elements = find_elements(driver=driver, field=field)
    return_element = None

    for element in elements:
        if element.text == text:
            log.debug(element.text)
            return_element = element
            break
        if element.get_attribute("value") == text:
            log.debug(element.get_attribute("value"))
            return_element = element
            break

    if return_element is None:
        raise NoSuchElementException("Element designed by field '{}' and text '{}'"
                                     " could not be located.".format(field, text))
    else:
        actions = ActionChains(driver)
        actions.move_to_element(return_element)
        actions.perform()
        return return_element


def find_sub_element_from_element(web_element=None, field=None):
    """
    Return a sub element from the element
    :param web_element:
    :param field:
    :return:
    """
    try:
        assert isinstance(web_element, WebElement), "web_element must be a WebElement object"
        assert isinstance(field, dict), "Field must be a dictionary"
        if "type" not in field.keys() or "value" not in field.keys():
            raise KeyError("The field argument doesn't contains either the 'type' or 'value' key.")

        switcher = {
            "id": web_element.find_element_by_id,
            "name": web_element.find_element_by_name,
            "class_name": web_element.find_element_by_class_name,
            "css": web_element.find_element_by_css_selector,
            "link_text": web_element.find_element_by_link_text,
            "partial_link_text": web_element.find_element_by_partial_link_text,
            "tag_name": web_element.find_element_by_tag_name,
            "xpath": web_element.find_element_by_xpath
            }

        element = switcher[field["type"]](field["value"])
        actions = ActionChains(web_element.parent)
        actions.move_to_element(element)
        actions.perform()
        return element
    except AssertionError as assertion:
        log.error("finders.find_sub_element_from_element raised an assertion with"
                  " following input\n web_element:'{}', field:'{}'. "
                  "Assertion is '{}'".format(web_element, field, assertion.args))
        raise
    except KeyError as key_error:
        log.error("In find_sub_element_from_element didn't find the method for '{}'"
                  " finder method".format(field["type"]))
        raise KeyError(key_error)
