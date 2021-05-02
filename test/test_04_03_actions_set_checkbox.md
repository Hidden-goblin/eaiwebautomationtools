# eaiautomatontools.actions.set_checkbox

Present the action utilities for Selenium automaton.
The set_checkbox method will update the status of the checkbox to match the expected one.

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

Import the set_checkbox tool

    >>> from eaiautomatontools.actions import set_checkbox

## Nominal case: all fields are valid

    >>> set_checkbox(driver=myWebDriver.webdriver, field={"type":"id","value":"check"}, is_checked=True)
    0

## Assertion errors

### The web driver is not given.

    >>> set_checkbox(field={"type":"id","value":"check"}, is_checked=True)
    Traceback (most recent call last):
    ...
    TypeError: Driver is expected

### The field is not valid

#### The keys are not one of "type" or "value"

    >>> set_checkbox(driver=myWebDriver.webdriver, field={"typ":"id","value":"check"}, is_checked=True)
    Traceback (most recent call last):
    ...
    KeyError: "The field argument doesn't contains either the 'type' or 'value' key."

#### Incorrect type key value not in

    >>> set_checkbox(driver=myWebDriver.webdriver, field={"type":"if","value":"check"}, is_checked=True)
    Traceback (most recent call last):
    ...
    ValueError: The field type is not one the expected: '('id', 'name', 'class_name', 'link_text', 'css', 'partial_link_text', 'xpath', 'tag_name')

#### is_checked is a boolean

    >>> set_checkbox(driver=myWebDriver.webdriver, field={"type":"id","value":"check"}, is_checked='True')
    Traceback (most recent call last):
    ...
    TypeError: is_checked is expected to be a boolean.

## Exception errors

### The element can't be found

    >>> set_checkbox(driver=myWebDriver.webdriver, field={"type":"id","value":"checkbox"}, is_checked=True)
    Traceback (most recent call last):
    ...
    selenium.common.exceptions.NoSuchElementException: Message: Element designed by field '{'type': 'id', 'value': 'checkbox'}' could not be located.
    <BLANKLINE>

### The element can't be checked

    >>> set_checkbox(driver=myWebDriver.webdriver, field={"type":"id","value":"name"}, is_checked=True)
    Traceback (most recent call last):
    ...
    Exception: The element '{'type': 'id', 'value': 'name'}' can't be set to the expected status 'True'.

Beware! Setting to False a non checkable element cast no error

    >>> set_checkbox(driver=myWebDriver.webdriver, field={"type":"id","value":"name"}, is_checked=False)
    0

## Teardown

    >>> myWebDriver.close()
    0

    >>> myWebDriver = None

    >>> myserver.stop()

    >>> myserver = None
