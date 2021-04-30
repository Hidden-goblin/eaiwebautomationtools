# eaiautomatontools.information.is_field_exist

Present the information utilities for Selenium automaton.
The is_field_exist method return a web element if the field is found or None if not found.


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

Import the information tool

    >>> from eaiautomatontools.information import is_field_exist


## Nominal case: give a web driver

### The field exists and is unique

    >>> element = is_field_exist(driver=myWebDriver.webdriver,field={"type":"id","value":"myIFrame"})

    >>> print(element) # doctest: +ELLIPSIS
    <selenium.webdriver.remote.webelement.WebElement ...

### The field doesn't exist

    >>> element = is_field_exist(driver=myWebDriver.webdriver,field={"type":"id","value":"myIFramed"})

    >>> print(element)
    None

### The field exist and is not unique

     >>> element = is_field_exist(driver=myWebDriver.webdriver,field={"type":"tag_name","value":"div"})

    >>> print(element) # doctest: +ELLIPSIS
    <selenium.webdriver.remote.webelement.WebElement ...

## Assertions

The web driver is mandatory

    >>> is_field_exist()
    Traceback (most recent call last):
    ...
    AssertionError: Driver is expected.


## Teardown

    >>> myWebDriver.close()
    0

    >>> myWebDriver = None

    >>> myserver.stop()

    >>> myserver = None
