# eaiautomatontools.alerts.intercept_alert

Present the alert utilities for Selenium automaton.
The intercept_alert method catches an alert popup (alert, confirm or prompt) and interact with it.
We can either accept/dismiss the alert, check the alert message, input a text in a prompt.

After using this method the alert is closed.

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

Import the element_text tool

    >>> from eaiautomatontools.information import element_text

Import the alerts tools

    >>> from eaiautomatontools.alerts import intercept_alert


## Nominal case: give a web driver, give a valid fields

### Alerts - javascript window.alert(message) command

Open the alert pop up

    >>> click_element(driver=myWebDriver.webdriver, field={"type":"id", "value":"button_alert"})
    0

### Accept the alert without any check

    >>> intercept_alert(driver=myWebDriver.webdriver)
    0

Open the alert pop up

    >>> click_element(driver=myWebDriver.webdriver, field={"type":"id", "value":"button_alert"})
    0

Accept the alert if the message is correct

    >>> intercept_alert(driver=myWebDriver.webdriver, messages=["A message from an alert.\nAnd a second line.",])
    0

Open the alert pop up

    >>> click_element(driver=myWebDriver.webdriver, field={"type":"id", "value":"button_alert"})
    0

Dismiss the alert

    >>> intercept_alert(driver=myWebDriver.webdriver, accept=False )
    0

### Confirms - javascript window.confirm(message) command

Open the alert pop up

    >>> click_element(driver=myWebDriver.webdriver, field={"type":"id", "value":"button_confirm"})
    0

Accept the alert without any check

    >>> intercept_alert(driver=myWebDriver.webdriver)
    0

The page displays "Confirmed"

    >>> element_text(driver=myWebDriver.webdriver, field={"type":"id","value":"prompt_return"})
    'Confirmed'

Open the alert pop up

    >>> click_element(driver=myWebDriver.webdriver, field={"type":"id", "value":"button_confirm"})
    0

Accept the alert if the message is correct

    >>> intercept_alert(driver=myWebDriver.webdriver, messages=["A message from an alert.\nAnd a second line.",])
    0

The page displays "Confirmed"

    >>> element_text(driver=myWebDriver.webdriver, field={"type":"id","value":"prompt_return"})
    'Confirmed'

Open the alert pop up

    >>> click_element(driver=myWebDriver.webdriver, field={"type":"id", "value":"button_confirm"})
    0

Dismiss the alert

    >>> intercept_alert(driver=myWebDriver.webdriver, accept=False )
    0

The page displays "Cancelled"

    >>> element_text(driver=myWebDriver.webdriver, field={"type":"id","value":"prompt_return"})
    'Cancelled'

### Prompt - javascript window.prompt(message,default) command

Open the alert pop up

    >>> click_element(driver=myWebDriver.webdriver, field={"type":"id", "value":"button_prompt"})
    0

Accept the alert without any check

    >>> intercept_alert(driver=myWebDriver.webdriver)
    0

The page displays the prompt default message

    >>> element_text(driver=myWebDriver.webdriver, field={"type":"id","value":"prompt_return"})
    'A default message'

Open the alert pop up

    >>> click_element(driver=myWebDriver.webdriver, field={"type":"id", "value":"button_prompt"})
    0

Dismiss the alert without any check

    >>> intercept_alert(driver=myWebDriver.webdriver, accept=False)
    0

The page displays no message

    >>> element_text(driver=myWebDriver.webdriver, field={"type":"id","value":"prompt_return"})
    ''

Open the alert pop up

    >>> click_element(driver=myWebDriver.webdriver, field={"type":"id", "value":"button_prompt"})
    0

Accept the alert checking its content

    >>> intercept_alert(driver=myWebDriver.webdriver, messages=["A message from an alert.\nAnd a second line.",])
    0

The page displays the prompt default message

    >>> element_text(driver=myWebDriver.webdriver, field={"type":"id","value":"prompt_return"})
    'A default message'


Open the alert pop up

    >>> click_element(driver=myWebDriver.webdriver, field={"type":"id", "value":"button_prompt"})
    0

Dismiss the alert checking its content

    >>> intercept_alert(driver=myWebDriver.webdriver, messages=["A message from an alert.\nAnd a second line.",], accept=False)
    0

The page displays no message

    >>> element_text(driver=myWebDriver.webdriver, field={"type":"id","value":"prompt_return"})
    ''

Open the alert pop up

    >>> click_element(driver=myWebDriver.webdriver, field={"type":"id", "value":"button_prompt"})
    0

Enter "My prompt is rich." in the alert and accept the alert

    >>> intercept_alert(driver=myWebDriver.webdriver, value="My prompt is rich.")
    0

The page displays the entered message

    >>> element_text(driver=myWebDriver.webdriver, field={"type":"id","value":"prompt_return"})
    'My prompt is rich.'

Open the alert pop up

    >>> click_element(driver=myWebDriver.webdriver, field={"type":"id", "value":"button_prompt"})
    0

Enter "My prompt is rich." in the alert and dismiss the alert

    >>> intercept_alert(driver=myWebDriver.webdriver, value="My prompt is rich.", accept=False)
    0

The page displays no message

    >>> element_text(driver=myWebDriver.webdriver, field={"type":"id","value":"prompt_return"})
    ''

## Assertions

### The web driver is mandatory

    >>> intercept_alert(value="My prompt is rich.", accept=False)
    Traceback (most recent call last):
    ...
    TypeError: Driver is expected

### The messages must be a string list

    >>> intercept_alert(driver=myWebDriver.webdriver, messages="toto")
    Traceback (most recent call last):
    ...
    TypeError: Messages should be a list or None

### The accept is a boolean

    >>> intercept_alert(driver=myWebDriver.webdriver, accept="True")
    Traceback (most recent call last):
    ...
    TypeError: Accept is boolean True or False

### Value is a string

    >>> intercept_alert(driver=myWebDriver.webdriver, value=True)
    Traceback (most recent call last):
    ...
    TypeError: Value is None or a string

## Exceptions

    >>> click_element(driver=myWebDriver.webdriver, field={"type":"id", "value":"button_alert"})
    0

### We raise an Exception if the alert is not one of the listed message.

    >>> intercept_alert(driver=myWebDriver.webdriver, messages=["toto",])
    Traceback (most recent call last):
    ...
    Exception: Message not found

###  We raise an ElementNotInteractableException if we try to enter a value in an alert which isn't a prompt.

    >>> intercept_alert(driver=myWebDriver.webdriver, value="toto" )
    Traceback (most recent call last):
    ...
    selenium.common.exceptions.ElementNotInteractableException: Message: Cannot found an input field
    <BLANKLINE>

    >>> intercept_alert(driver=myWebDriver.webdriver)
    0

### There is no alert to interact with.

    >>> intercept_alert(driver=myWebDriver.webdriver)
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
