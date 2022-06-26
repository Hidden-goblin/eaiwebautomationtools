# eaiautomatontools.information.element_text

Present the information utilities for Selenium automaton.
The element_text method returns:
    - the field text or its value if only one of them is set or both have the same text
    - '' if there is no text or value
    - an Exception if the text and the value differs.



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

    >>> myWebDriver.go_to("http://localhost:8081/forms.html")
    0

Import the fill field tool

    >>> from eaiautomatontools.actions import fill_element

Import the information tool

    >>> from eaiautomatontools.information import element_text


## Nominal case: give a web driver

### The field text exist but not the value

    >>> element_text(driver=myWebDriver.webdriver, field={"type":"id", "value":"lab-name"})
    'Enter your name:'

### The field text doesn't exist but the value exists

    >>> element_text(driver=myWebDriver.webdriver, field={"type":"id", "value":"labelless-button"})
    'label'

### Both the field text and the value exit and the text are the same

    >>> element_text(driver=myWebDriver.webdriver, field={"type":"id", "value":"email"})
    'Your.mail@he.re'

### There is no text or attribute 'value'

    >>> element_text(driver=myWebDriver.webdriver, field={"type":"id", "value":"span"})
    ''

## Assertions

The web driver is mandatory

    >>> element_text()
    Traceback (most recent call last):
    ...
    TypeError: Driver is expected


## Exception

    >>> element_text(driver=myWebDriver.webdriver, field={"type":"id", "value":"one-button"})
    Traceback (most recent call last):
    ...
    Exception: Can't serve the element 'text' having both data for text and attribute value

## Teardown

    >>> myWebDriver.close()
    0

    >>> myWebDriver = None

    >>> myserver.stop()

    >>> myserver = None
