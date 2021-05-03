# eaiautomatontools.alerts.alert_message

Present the alerts utilities for Selenium automaton.
The alert_message method return the alert message.

It will raise an exception if there is no alert to retrieve the message from.


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
    0
  
  

Open the form test page

    >>> myWebDriver.go_to("http://localhost:8081")
    0

Import the click tool

    >>> from eaiautomatontools.actions import click_element

Import the alerts tools

    >>> from eaiautomatontools.alerts import alert_message, intercept_alert


## Nominal case: give a web driver

### Alerts - javascript window.alert(message) command

Open the alert pop up

    >>> click_element(driver=myWebDriver.webdriver, field={"type":"id", "value":"button_alert"})
    0

Retrieve the alert message

    >>> alert_message(driver=myWebDriver.webdriver)
    'A message from an alert.\nAnd a second line.'

Accept the alert without any check

    >>> intercept_alert(driver=myWebDriver.webdriver)
    0

### Confirms - javascript window.confirm(message) command

Open the alert pop up

    >>> click_element(driver=myWebDriver.webdriver, field={"type":"id", "value":"button_confirm"})
    0

Retrieve the alert message

    >>> alert_message(driver=myWebDriver.webdriver)
    'A message from an alert.\nAnd a second line.'


Accept the alert without any check

    >>> intercept_alert(driver=myWebDriver.webdriver)
    0

### Prompt - javascript window.prompt(message,default) command

Open the alert pop up

    >>> click_element(driver=myWebDriver.webdriver, field={"type":"id", "value":"button_prompt"})
    0

Retrieve the alert message

    >>> alert_message(driver=myWebDriver.webdriver)
    'A message from an alert.\nAnd a second line.'

Accept the alert without any check

    >>> intercept_alert(driver=myWebDriver.webdriver)
    0

## Assertions

The web driver is mandatory

    >>> alert_message()
    Traceback (most recent call last):
    ...
    TypeError: Driver is expected


## Exceptions

There is no alert to interact with.

    >>> alert_message(driver=myWebDriver.webdriver)
    Traceback (most recent call last):
    ...
    selenium.common.exceptions.NoAlertPresentException: Message: Can't interact with an alert as there is no displayed alert
    <BLANKLINE>

## Teardown

    >>> myWebDriver.close()
    0

    >>> myWebDriver = None

    >>> myserver.stop()

    >>> myserver = None
