# Could held the webdriver instance so that we could interact with the browser.
# -*- coding: utf-8 -*-
import os.path
import json
import logging
import tempfile
from shutil import rmtree
from datetime import datetime
from selenium import webdriver
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
    is_checkbox_checked
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
        self.__authorized_name_version = ["chrome", "firefox", "opera",
                                          "edge", "safari"]
        # All strings allowed for the browser name and version

        self.__launched = False
        self.__location = None
        # Refactoring using webdriver manager
        # os.path.normpath(
        # "{0}{1}webdrivers".format(os.path.dirname(__file__),
        #                           os.path.sep))  # The default web driver folder

        self.__temp_save_to = os.path.normpath(os.path.join(tempfile.gettempdir(),
                                                            "automaton_screenshots"))
        if not os.path.exists(self.__temp_save_to):
            os.makedirs(self.__temp_save_to)
        else:
            rmtree(self.__temp_save_to)
            os.makedirs(self.__temp_save_to)

        log.debug(self.__temp_save_to)
        # Definition of public attributes
        self.__webdriver = None
        self.__browser_name = None
        self.__driver_path = None

    @property
    def webdriver(self):
        return self.__webdriver

    @property
    def browser_name(self):
        return self.__browser_name

    @browser_name.setter
    def browser_name(self, name):
        if name in self.__authorized_name_version:
            self.__browser_name = name
        else:
            raise ValueError(f"Unknown browser name. Get {name} instead of {self.__authorized_name_version}")

    @property
    def driver_path(self):
        return self.__driver_path

    @driver_path.setter
    def driver_path(self, new_path):
        if new_path is not None and new_path:
            if os.path.exists(new_path):
                self.__driver_path = new_path
            else:
                raise ValueError("Expecting an existing file")
        else:
            raise ValueError("Expecting a non empty path")
        # with open(os.path.join(self.__location, "webdriver.json")) as file:
        #     self.__webdriver_mapping = json.load(file)
        # self.__initiate_webdriver_mapping()
        # log.info("Browser server instantiate")

    # def __initiate_webdriver_mapping(self):
    #     """
    #     Initiate the webdriver mapping by creating the full path to the webdriver executable.
    #     :return:
    #     """
    #     for browser in self.__webdriver_mapping.keys():
    #         for version in self.__webdriver_mapping[browser].keys():
    #             self.__webdriver_mapping[browser][version] = \
    #                 os.path.normpath("{}{}{}".format(self.__location,
    #                                                  os.path.sep,
    #                                                  self.__webdriver_mapping[browser][version]))

    def update_webdriver_mapping(self, new_mapping=None):
        """
        Update the mapping in order to use other webdriver executable.
        :param new_mapping: a dictionary {<browser>:{<version>:driver absolute path,...}...}
        :raise AssertError: if the mapping isn't correct.
        :raise AssertError: if the webdriver file doesn't exist
        :return:
        """
        assert isinstance(new_mapping, dict), "The new mapping is a dictionary " \
                                              "{<browser>:{<version>:driver absolute path,...}...}"
        assert all((key in self.__authorized_name_version for key in new_mapping.keys())), \
            "The browsers should be one of '{}'".format(self.__authorized_name_version)
        for browser in new_mapping.keys():
            assert isinstance(new_mapping[browser], dict), \
                "The browser is described as a dictionary {<version>:driver absolute path,...}"
            assert all((key in self.__authorized_name_version for
                        key in new_mapping[browser].keys())), \
                "The versions should be one of 32 or 64"
            for version in new_mapping[browser].keys():
                assert os.path.isfile(new_mapping[browser][version]), \
                    "File '{}' doesn't exist".format(new_mapping[browser][version])
                try:
                    self.__webdriver_mapping[browser][version] = new_mapping[browser][version]
                except KeyError:  # First time we access the value. We add directly a dictionary
                    self.__webdriver_mapping[browser] = {version: new_mapping[browser][version]}

    def set_browser_type(self, name=None, version=None, browser_type=None):
        """
        Set the browser type and version (32-64bits) for launching a webdriver
        :param name:
        :param version:
        :param browser_type:
        :return: 0 if success
        """
        if browser_type is not None and isinstance(browser_type, dict):
            if all([key in browser_type.keys() for key in ["name", "version"]]) \
                    and all([value in self.__authorized_name_version for
                             value in browser_type.values()]):
                self.browser_type = browser_type
            else:
                raise KeyError("browser is defined by his name and his version (32, 64bits)")
        elif name is not None and \
                version is not None and \
                name in self.__authorized_name_version and \
                version in self.__authorized_name_version:
            self.browser_type["name"] = name
            self.browser_type["version"] = version
        else:
            log.exception("TypeError exception raised in BrowserServer.set_browser_type. "
                          "Received name:'{}', version:'{}' "
                          "browser_type:'{}'".format(name, version, browser_type))
            raise TypeError("name and version cannot be None "
                            "or browser_type cannot be None or not a dictionary")
        return 0

    @staticmethod
    def __driver_switcher():
        """
        Switcher method providing the webdriver to process
        :return: A webdriver method
        """
        return {
            "chrome": webdriver.Chrome,
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
            "firefox": GeckoDriverManager,
            "edge": EdgeChromiumDriverManager,
            "opera": OperaDriverManager
        }

    @staticmethod
    def __serve_time():
        datetime_object = datetime.now()
        return int(datetime_object.timestamp() * 1000000)

    def serve(self):
        """
        Create the webdriver instance
        Todo incorportate the outside module resources locator
        :return: 0 if success
        """
        # todo use the data in order to launch the expected webdriver
        # if all([value in self.__authorized_name_version for value in self.browser_type.values()]):
        #     webdriver_path = os.path.normpath(os.path.join(self.__location,
        #                                                    self.__webdriver_mapping[
        #                                                        self.browser_type["name"]][
        #                                                        self.browser_type["version"]]))
        #     if not os.path.isfile(webdriver_path):
        #         raise FileNotFoundError("{} is not a valid file.".format(webdriver_path))
        #
        #     self.webdriver = \
        #         self.__driver_switcher()[self.browser_type["name"]](
        #             executable_path=self.__webdriver_switcher()[self.browser_type["name"]]().install())
        #     self.__launched = True
        # else:
        #     log.exception("Browser type not defined. Received browser:'{}', version:'{}' Expected "
        #                   "values from '{}'".format(self.browser_type["name"],
        #                                             self.browser_type["version"],
        #                                             self.__authorized_name_version))
        #     raise ValueError("Browser type not defined."
        #                      " Could be one of '{}'".format(self.__authorized_name_version))

        if self.browser_name != "safari":
            self.__webdriver = \
                self.__driver_switcher()[self.browser_name](
                    executable_path=self.__webdriver_switcher()[self.browser_name]().install())
            self.__launched = True
        else:
            self.__webdriver = self.__driver_switcher()[self.browser_name](executable_path=self.driver_path)
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

    def get(self):
        """
        Return the webdriver instance
        :return: the current webdriver
        """
        return self.webdriver

    def full_screenshot(self, filename):
        result = fullpage_screenshot(self.webdriver, filename)
        return result

    def take_a_screenshot(self, save_to=None, full_screen='yes'):
        """
        Take a screenshot and save the file to the given folder
        Each screenshot is followed by a timestamp.
        :param full_screen:
        :param save_to:
        :return: 0 if success
        """
        screenshot_switcher = {
            'yes': self.full_screenshot,
            'no': self.webdriver.get_screenshot_as_file
        }
        if full_screen.lower() not in screenshot_switcher:
            log.warning("full_screen should be 'yes' (default) or 'no'. Received: {}".format(
                                                                                  full_screen))
            full_screen = 'yes'
        try:
            filename = ''
            if save_to is None:
                filename = os.path.join(
                    self.__temp_save_to, "screenshot-{}.png".format(self.__serve_time()))
            else:
                log.debug("Try to save to '{}'".format(save_to))
                filename = os.path.join(save_to, "screenshot-{}.png".format(self.__serve_time()))
            result = screenshot_switcher[full_screen](filename)
            if not result:
                log.error("The screenshot could not be done."
                          " Please check if the file path is correct."
                          " Get '{}'".format(repr(result)))
                raise IOError("The screenshot could not be done."
                              " Please check if the file path is correct."
                              " Get '{}'".format(repr(result)))
            return 0
        except IOError as io_error:
            raise IOError(io_error.args[0]) from None
        except Exception as exception:
            log.error("Screenshot raised an error '{}'".format(exception.args[0]))
            raise Exception(exception.args[0]) from None

    # Start  of convenient usage of the automaton tools
    # Navigation

    def go_to(self, url=None):
        return go_to_url(driver=self.webdriver, url=url)

    def enter_frame(self, field=None):
        return enter_frame(driver=self.webdriver, field=field)

    def go_to_window(self, handle=None, title=None):
        return go_to_window(driver=self.webdriver, handle=handle, title=title)

    # Finders

    def find_element(self, field=None):
        return find_element(driver=self.webdriver, field=field)

    def find_elements(self, field=None):
        return find_elements(driver=self.webdriver, field=field)

    def find_from_elements(self, field=None, text=None):
        return find_from_elements(driver=self.webdriver, field=field, text=text)

    def find_sub_element_from_element(self, field=None):
        """
        Find the webelement contained in another webelement.
        If no parent is provided try to return the webelement
        :param field:
        :return:
        """
        if "parent" in field:
            element = self.find_element(field=field["parent"])
            return find_sub_element_from_element(element, field=field)
        else:
            return self.find_element(field=field)

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

    # TODO add unit test
    def where_am_i(self):
        return where_am_i(driver=self.webdriver)

    # TODO add unit test
    def is_checkbox_checked(self, field=None, is_angular=False):
        return is_checkbox_checked(driver=self.webdriver, field=field, is_angular=is_angular)

