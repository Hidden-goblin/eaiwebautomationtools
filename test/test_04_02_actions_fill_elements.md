# eaiautomatontools.actions.fill_elements

Present the action utilities for Selenium automaton.
The fill_elements method try to locate elements and fill them with the value stored in data. We assume each element can receive a text.
It will raise an exception if it's not the case.
This method is interesting when fields and data are stored as dictionaries.

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

    >>> myWebDriver.go_to("http://localhost:8081/forms.html")
    0

Import the find_element tool

    >>> from eaiautomatontools.finders import find_element

Import the fill_element tool

    >>> from eaiautomatontools.actions import fill_elements



## Nominal case: give a web driver, give a valid fields

We will fill the username field with "my name" and the email field with "my.email@test.com".

    >>> fill_elements(driver=myWebDriver.webdriver, fields={"username":{"type":"id","value":"name"}, "email":{"type":"id","value":"email"}},data={"username":"my name","email":"my.email@test.com"})
    0

## Assertions

### The web driver is mandatory

    >>> fill_elements(fields={"username":{"type":"id","value":"name"}, "email":{"type":"id","value":"email"}},data={"username":"my name","email":"my.email@test.com"})
    Traceback (most recent call last):
    ...
    TypeError: Driver is expected

### Fields dictionary and data dictionary contain the same keys.

    >>> fill_elements(driver=myWebDriver.webdriver, fields={"user":{"type":"id","value":"name"}, "email":{"type":"id","value":"email"}},data={"username":"my name","email":"my.email@test.com"})
    Traceback (most recent call last):
    ...
    KeyError: 'Data keys are not included in Fields keys'

## Exceptions

### One field doesn't exist on the UI

    >>> fill_elements(driver=myWebDriver.webdriver, fields={"username":{"type":"id","value":"uname"}, "email":{"type":"id","value":"email"}},data={"username":"my name","email":"my.email@test.com"})
    1

### One field isn't user-editable

    >>> fill_elements(driver=myWebDriver.webdriver, fields={"username":{"type":"id","value":"lab-name"}, "email":{"type":"id","value":"email"}},data={"username":"my name","email":"my.email@test.com"})
    1

## Teardown

    >>> myWebDriver.close()
    0

    >>> myWebDriver = None

    >>> myserver.stop()

    >>> myserver = None
