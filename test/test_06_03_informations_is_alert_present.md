# eaiautomatontools.information.is_alert_present

Present the information utilities for Selenium automaton.
The is_alert_present method return True if an alert is present.


## Background

Launch a test web server serving controlled web pages on localhost port 8081

Use the python resources server.

    >>> from eaiautomatontools.resources.app import Server

    >>> myserver = Server()

    >>> myserver.start()
    ...

Instantiate a web driver using the eaiautomatontools.browserServer

    >>> from eaiautomatontools.browserServer import BrowserServer

    >>> myWebDriver = BrowserServer()

Use a default browser such as Chrome in 32 bit version

    >>> myWebDriver.browser_name = "chrome"

Serve the web driver

    >>> myWebDriver.serve()
    <BLANKLINE>
    0
  

Open the form test page

    >>> myWebDriver.go_to("http://localhost:8081")
    0

Import the fill field tool

    >>> from eaiautomatontools.actions import click_element

Import the information tool

    >>> from eaiautomatontools.information import is_alert_present

Import the alert tool

    >>> from eaiautomatontools.alerts import intercept_alert

## Nominal case: give a web driver

### No alert present.

    >>> is_alert_present(driver=myWebDriver.webdriver)
    False

### An alert is present.

    >>> click_element(driver=myWebDriver.webdriver, field={"type":"id", "value":"button_alert"})
    0

    >>> is_alert_present(driver=myWebDriver.webdriver)
    True


## Assertions

The web driver is mandatory

    >>> is_alert_present()
    Traceback (most recent call last):
    ...
    TypeError: Driver is expected


## Teardown

    >>> myWebDriver.close()
    0

    >>> myWebDriver = None

    >>> myserver.stop()

    >>> myserver = None
