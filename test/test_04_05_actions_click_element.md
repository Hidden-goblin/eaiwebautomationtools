# eaiautomatontools.actions.click_element

Present the action utilities for Selenium automaton.
The click_element method will perform a mouse left click action.

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

Import the find_element tool

    >>> from eaiautomatontools.finders import find_element

Import the set_checkbox tool

    >>> from eaiautomatontools.actions import click_element

## Nominal case: give a web driver, give a valid field

You can click a link

    >>> click_element(driver=myWebDriver.webdriver,field={'type':'id','value':'tables'})
    0

    >>> myWebDriver.go_to("http://localhost:8081")
    0

You can even click a div

    >>> click_element(driver=myWebDriver.webdriver,field={'type':'id','value':'first'})
    0

## Assertions

###  The web driver is missing.
    >>> click_element(field={"type":"id", "value":"name"})
    Traceback (most recent call last):
    ...
    AssertionError: Driver is expected.

### The field is not valid.

#### Incorrect type key value.

    >>> click_element(driver=myWebDriver.webdriver, field={"type":"idl", "value":"name"})
    Traceback (most recent call last):
    ...
    AssertionError: Field '{'type': 'idl', 'value': 'name'}' is not a valid field

#### Incorrect keys value.

    >>> click_element(driver=myWebDriver.webdriver, field={"typ":"id", "value":"name"})
    Traceback (most recent call last):
    ...
    AssertionError: Field '{'typ': 'id', 'value': 'name'}' is not a valid field

## Exceptions

    >>> click_element(driver=myWebDriver.webdriver,field={'type':'id','value':'tab'})
    Traceback (most recent call last):
    ...
    Exception: Element designed by field '{'type': 'id', 'value': 'tab'}' could not be located.

## Teardown

    >>> myWebDriver.close()
    0

    >>> myWebDriver = None

    >>> myserver.stop()

    >>> myserver = None
