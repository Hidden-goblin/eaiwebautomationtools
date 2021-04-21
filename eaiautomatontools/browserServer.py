# Could held the webdriver instance so that we could interact with the browser.
# -*- coding: utf-8 -*-
import os.path
import logging
import tempfile
from deprecated import deprecated
from shutil import rmtree
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.opera import OperaDriverManager
from .navigators import go_to_url, enter_frame, go_to_window
from .finders import find_element, find_elements, find_from_elements, \
    find_sub_element_from_element
from .actions import fill_element, fill_elements, select_in_dropdown, set_checkbox, \
    click_element, select_in_angular_dropdown, hover_element, select_in_elements
from .alerts import alert_message, intercept_alert
from .information import is_alert_present, is_field_exist, is_field_contains_text, \
    element_text, is_field_displayed, is_field_enabled, how_many_windows, where_am_i, \
    is_checkbox_checked, retrieve_tabular
from .drivers_tools import fullpage_screenshot

log = logging.getLogger(__name__)


class BrowserServer:
    """
    The BrowserServer is a convenient object which instantiate a selenium web driver.
    It serves all automaton tools such as finders, actions, alert and navigators.
    Although these tools can be used separately and are tested separately,
    it will be easier to use them from this class.
    Please see the eaiautomatontools specific doctest.
    Todo set others webdriver executables
    """

    def __init__(self):
        # Definition of private attributes and references
        # All strings allowed for the browser name and version
        self.__authorized_name_version = ("chrome", "firefox", "opera",
                                          "edge", "safari", "headless-chrome")
        # Browser window's status
        self.__launched = False

        # Screenshot save folder
        self.__temp_save_to = os.path.normpath(os.path.join(tempfile.gettempdir(),
                                                            "automaton_screenshots"))
        if os.path.exists(self.__temp_save_to):
            rmtree(self.__temp_save_to)
        os.makedirs(self.__temp_save_to)
        log.debug(self.__temp_save_to)

        # Definition of private attributes
        self.__webdriver = None  # The webdriver
        self.__browser_name = None  # The browser's name used
        self.__driver_path = None  # The path to the webdriver executable
    
    @property
    def is_launched(self):
        return self.__launched

    @property
    def webdriver(self):
        """Read only webdriver"""
        return self.__webdriver

    @property
    def browser_name(self):
        """Read - Set browser name with restrictions"""
        return self.__browser_name

    @browser_name.setter
    def browser_name(self, name: str):
        if name.casefold() not in self.__authorized_name_version:
            raise ValueError(f"Unknown browser name. "
                             f"Get {name.casefold()} instead of {self.__authorized_name_version}")
        self.__browser_name = name.casefold()
        self.__driver_path = None

    @property
    def driver_path(self):
        return self.__driver_path

    @driver_path.setter
    def driver_path(self, new_path: str):
        if new_path is not None and new_path:
            if os.path.exists(new_path):
                self.__driver_path = new_path
            else:
                raise ValueError("Expecting an existing file")
        else:
            raise ValueError("Expecting a non empty path")

    @staticmethod
    def __driver_switcher():
        """
        Switcher method providing the webdriver to process
        :return: A webdriver method
        """
        return {
            "chrome": webdriver.Chrome,
            "headless-chrome": webdriver.Chrome,
            "firefox": webdriver.Firefox,
            "edge": webdriver.Edge,
            "safari": webdriver.Safari,
            "opera": webdriver.Opera
        }

    @staticmethod
    def __webdriver_switcher():
        """

        :return:
        """
        return {
            "chrome": ChromeDriverManager,
            "headless-chrome": ChromeDriverManager,
            "firefox": GeckoDriverManager,
            "edge": EdgeChromiumDriverManager,
            "opera": OperaDriverManager
        }

    @staticmethod
    def __serve_time():
        return int(datetime.now().timestamp() * 1000000)

    def serve(self):
        """
        Create the webdriver instance
        Todo incorporate the outside module resources locator
        TODO Handle the case where you don't want to use the webdriver manager
        :return: 0 if success
        """
        # todo use the data in order to launch the expected webdriver
        if self.browser_name == "safari":
            self.__webdriver = self.__driver_switcher()[self.browser_name](
                executable_path=self.driver_path)
        elif self.browser_name == "chrome":
            # Hack https://stackoverflow.com/questions/64927909/
            # failed-to-read-descriptor-from-node-connection-a-device-attached-to-the-system
            if self.__driver_path is None:
                self.__driver_path = self.__webdriver_switcher()[self.browser_name]().install() 
            option = Options()
            option.add_experimental_option('excludeSwitches', ['enable-logging'])
            self.__webdriver = \
                self.__driver_switcher()[self.browser_name](
                    executable_path=self.__driver_path,
                    options=option
                )
        elif self.browser_name == "headless-chrome":
            option = Options()
            option.add_experimental_option('excludeSwitches', ['enable-logging'])
            option.headless = True
            if self.__driver_path is None:
                self.__driver_path = self.__webdriver_switcher()[self.browser_name]().install()
            self.__webdriver = \
                self.__driver_switcher()[self.browser_name](
                    executable_path=self.__driver_path,
                    options=option
                )
        elif self.browser_name is not None:
            if self.__driver_path is None:
                self.__driver_path = self.__webdriver_switcher()[self.browser_name]().install()
            self.__webdriver = \
                self.__driver_switcher()[self.browser_name](
                    executable_path=self.__driver_path)

        else:
            raise AttributeError("You must set a browser name. "
                                 f"Use one of '{self.__authorized_name_version}'")
        self.__launched = True
        return 0

    def close(self):
        """
        Close the webdriver
        :return:
        """
        self.webdriver.quit()
        self.__webdriver = None
        self.__launched = False
        return 0

    def full_screenshot(self, filename: str):
        return fullpage_screenshot(self.webdriver, filename)

    def take_a_screenshot(self, save_to: str = None, is_full_screen: bool = True):
        """
        Take a screenshot and save the file to the given folder
        Each screenshot is followed by a timestamp.
        :param is_full_screen:
        :param save_to:
        :return: 0 if success
        """
        try:
            # Process the filename
            if save_to is None:
                filename = os.path.join(
                    self.__temp_save_to, "screenshot-{}.png".format(self.__serve_time()))
            else:
                log.debug("Try to save to '{}'".format(save_to))
                filename = os.path.join(save_to, "screenshot-{}.png".format(self.__serve_time()))
            if is_full_screen:
                result = self.full_screenshot(filename)
            else:
                result = self.webdriver.get_screenshot_as_file(filename)
            if not result:
                log.error("The screenshot could not be done."
                          " Please check if the file path is correct."
                          " Get '{}'".format(repr(result)))
                raise IOError("The screenshot could not be done."
                              " Please check if the file path is correct."
                              " Get '{}'".format(repr(result)))
            return os.path.realpath(filename)
        except IOError as io_error:
            log.error(f"Screenshot raised an IO error '{io_error.args[0]}'")
            raise IOError(io_error.args[0]) from None
        except Exception as exception:
            log.error(f"Screenshot raised an error '{exception.args[0]}'")
            raise Exception(exception.args[0]) from None

    # Start of convenient usage of the automaton tools
    # Navigation

    def go_to(self, url=None):
        return go_to_url(driver=self.webdriver, url=url)

    def enter_frame(self, field=None):
        return enter_frame(driver=self.webdriver, field=field)

    def go_to_window(self, handle=None, title=None):
        return go_to_window(driver=self.webdriver, handle=handle, title=title)

    # Finders
    def find_element(self, field: dict = None, web_element: WebElement = None):
        """Find element using the current webdriver or the provided WebElement"""
        return find_element(driver=self.webdriver, field=field, web_element=web_element)

    def find_elements(self, field: dict = None, web_element: WebElement = None):
        """Find elements using the current webdriver or the provided WebElement"""
        return find_elements(driver=self.webdriver, field=field, web_element=web_element)

    def find_from_elements(self, field=None, text=None, web_element: WebElement = None):
        """Find element from a list of elements based on the text (exact match)"""
        return find_from_elements(driver=self.webdriver,
                                  field=field,
                                  text=text,
                                  web_element=web_element)

    @deprecated(version="1.0.5", reason="You should user find_element with a web_element")
    def find_sub_element_from_element(self, field=None):
        """
        Find the webelement contained in another webelement.
        If no parent is provided try to return the webelement
        :param field:
        :return:
        """
        if "parent" not in field:
            return self.find_element(field=field)
        element = self.find_element(field=field["parent"])
        return find_sub_element_from_element(element, field=field)

    # Actions

    def fill_element(self, field=None, value=None):
        return fill_element(driver=self.webdriver, field=field, value=value)

    def fill_elements(self, fields=None, data=None):
        return fill_elements(driver=self.webdriver, fields=fields, data=data)

    # TODO add unit test
    def click_element(self, field=None, inner_element_to_click=None):
        return click_element(driver=self.webdriver,
                             field=field,
                             inner_element_to_click=inner_element_to_click)

    def select_in_dropdown(self, field=None, visible_text=None, value=None):
        return select_in_dropdown(driver=self.webdriver,
                                  field=field,
                                  visible_text=visible_text,
                                  value=value)

    # TODO add unit test
    def select_in_angular_dropdown(self, root_field=None, visible_text=None):
        return select_in_angular_dropdown(driver=self.webdriver,
                                          root_field=root_field,
                                          visible_text=visible_text)

    def set_checkbox(self, field=None, is_checked=None):
        return set_checkbox(driver=self.webdriver,
                            field=field,
                            is_checked=is_checked)

    # TODO add unit test
    def hover_element(self, field=None):
        return hover_element(driver=self.webdriver, field=field)

    # TODO add unit test
    def select_in_elements(self, field=None, displayed_text=None):
        return select_in_elements(driver=self.webdriver,
                                  field=field,
                                  displayed_text=displayed_text)

    # Alerts
    def alert_message(self):
        return alert_message(driver=self.webdriver)

    def intercept_alert(self, messages=None, accept=True, value=None):
        return intercept_alert(driver=self.webdriver, messages=messages,
                               accept=accept, value=value)

    # Information

    def is_alert_present(self, until=5):
        return is_alert_present(driver=self.webdriver, until=until)

    def is_field_exist(self, field=None, until=5):
        return is_field_exist(driver=self.webdriver, field=field, until=until)

    def is_field_contains_text(self, field=None, text=None):
        return is_field_contains_text(driver=self.webdriver, field=field, text=text)

    def element_text(self, field=None):
        return element_text(driver=self.webdriver, field=field)

    def is_field_displayed(self, field=None):
        return is_field_displayed(driver=self.webdriver, field=field)

    def is_field_enabled(self, field=None, attribute=None):
        return is_field_enabled(driver=self.webdriver, field=field, attribute=attribute)

    def how_many_windows(self):
        return how_many_windows(driver=self.webdriver)

    def retrieve_tabular(self, field=None, row_and_col=("tr", "td", "th")):
        return retrieve_tabular(driver=self.webdriver, field=field, row_and_col=row_and_col)

    # TODO add unit test
    def where_am_i(self):
        return where_am_i(driver=self.webdriver)

    # TODO add unit test
    def is_checkbox_checked(self, field=None, is_angular=False):
        return is_checkbox_checked(driver=self.webdriver, field=field, is_angular=is_angular)

