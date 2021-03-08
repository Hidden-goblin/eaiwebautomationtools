# -*- coding: utf-8 -*-
import logging
from selenium.common.exceptions import ElementNotSelectableException, NoAlertPresentException
from .drivers_tools import web_drivers_tuple


def intercept_alert(driver=None, messages=None, accept=True, value=None):
    """
        intercept_alert goal is to provide an easy interface to handle alerts.

        Only the web driver is mandatory.

        Giving only the web driver accept the alert whatever the message is.

        Giving a list of messages, ensure that the alert message is one of the list.
    :param value: The string to be entered in the prompt alert.
    :param driver: a selenium webdriver
    :param messages: A list of string which should include the alert message.
    :param accept: boolean defaulted to True. Accept or dismiss the alert.
    :raise AssertionError: driver, messages, accept and value aren't of the expected type
    :raise ElementNotSelectableException: when trying to send keys on a non-prompt alert
    :raise NoAlertPresentException: when trying to intercept an alert which not present
    :raise Exception: when the alert message is not one of the expected
    :return: 0 if success
    """
    try:
        assert driver is not None and isinstance(driver, web_drivers_tuple()), "Driver is expected."
        assert messages is None or isinstance(messages, list), "Messages should be a list or None"
        assert isinstance(accept, bool), "Accept is boolean True or False"
        assert value is None or isinstance(value, str), "Value is None or a string"

        alert_object = driver.switch_to.alert

        if messages is not None and isinstance(messages, list):
            if alert_object.text not in messages:
                raise Exception("Message not found")

        if value is not None:
            alert_object.send_keys(value)

        if accept:
            alert_object.accept()
        else:
            alert_object.dismiss()

        return 0
    except AssertionError as assertion:
        logging.error("alerts.intercept_alert raised an assertion with following"
                      " input driver:'{}', message:'{}' and accept:'{}'."
                      " Assertion is '{}'".format(driver, messages, accept, assertion.args))
        raise
    except ElementNotSelectableException as not_selectable:
        logging.error("alerts.intercept_alert can't fill the alert popup with '{}'"
                      " as there is no input field.\nGet {}".format(value, not_selectable.args))
        raise ElementNotSelectableException(
            "Can't fill the alert popup with '{}' as there is no "
            "input field.".format(value)) from None
    except NoAlertPresentException as no_alert:
        logging.error(
            "alerts.intercept_alert can't interact with an alert as there is no "
            "displayed alert.\nGet {}".format(no_alert.args))
        raise NoAlertPresentException("Can't interact with an alert as there is no "
                                      "displayed alert") from None


def alert_message(driver=None):
    """
        Return the message displayed in the alert.
    :param driver: a selenium webdriver
    :raise AssertionError: driver isn't of the expected type
    :raise NoAlertPresentException: when trying to intercept an alert which not present
    :return: 0 if success
    """
    try:
        assert driver is not None and isinstance(driver, web_drivers_tuple()), "Driver is expected."
        alert_object = driver.switch_to.alert

        return alert_object.text
    except AssertionError as assertion:
        logging.error("alerts.alert_message raised an assertion with following input"
                      " driver:'{}'. Assertion is '{}'".format(driver, assertion.args))
        raise
    except NoAlertPresentException as no_alert:
        logging.error("alerts.intercept_alert can't interact with an alert as there"
                      " is no displayed alert.\nGet {}".format(no_alert.args))
        raise NoAlertPresentException("Can't interact with an alert as there is no"
                                      " displayed alert") from None
