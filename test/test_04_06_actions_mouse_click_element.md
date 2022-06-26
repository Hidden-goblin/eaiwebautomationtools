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
    <BLANKLINE>
    0
  
  

Open the form test page

    >>> myWebDriver.go_to("http://localhost:8081")
    0


Import the mouse_click tool

    >>> from eaiautomatontools.actions import mouse_click

## Nominal case: give a web driver, give a valid field

You can click a link

    >>> mouse_click(driver=myWebDriver.webdriver,field={'type':'id','value':'tables'})
    0

    >>> myWebDriver.webdriver.current_url
    'http://localhost:8081/tables.html'

You can even click a div

    >>> myWebDriver.go_to("http://localhost:8081")
    0

    >>> mouse_click(driver=myWebDriver.webdriver,field={'type':'id','value':'first'})
    0

    >>> myWebDriver.webdriver.current_url
    'http://localhost:8081/'

## Assertions

###  The web driver is missing.
    >>> mouse_click(field={"type":"id", "value":"name"})
    Traceback (most recent call last):
    ...
    TypeError: Driver is expected

### The field is not valid.

#### Incorrect type key value.

    >>> mouse_click(driver=myWebDriver.webdriver, field={"type":"idl", "value":"name"})
    Traceback (most recent call last):
    ...
    ValueError: The field type is not one the expected: '('id', 'name', 'class_name', 'link_text', 'css', 'partial_link_text', 'xpath', 'tag_name')

#### Incorrect keys value.

    >>> mouse_click(driver=myWebDriver.webdriver, field={"typ":"id", "value":"name"})
    Traceback (most recent call last):
    ...
    KeyError: "The field argument doesn't contains either the 'type' or 'value' key."

## Exceptions

    >>> mouse_click(driver=myWebDriver.webdriver,field={'type':'id','value':'tab'})
    1

## Teardown

    >>> myWebDriver.close()
    0

    >>> myWebDriver = None

    >>> myserver.stop()

    >>> myserver = None
