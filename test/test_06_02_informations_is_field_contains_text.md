# eaiautomatontools.information.is_field_contains_text

Present the information utilities for Selenium automaton.
The is_field_contains_text method return True if the field or its value contains the text.


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

Import the fill field tool

    >>> from eaiautomatontools.actions import fill_element

Import the information tool

    >>> from eaiautomatontools.information import is_field_contains_text


## Nominal case: give a web driver

### The field contains the text.

    >>> is_field_contains_text(driver=myWebDriver.webdriver,field={"type":"id","value":"lab-name"}, text="Enter your name:")
    True

### The field doesn't contains the text.

    >>> is_field_contains_text(driver=myWebDriver.webdriver,field={"type":"id","value":"lab-name"}, text="Your name:")
    False

### The field contains the text. The text may be a part of the field text. Beware, as the example b shows, this is case sensitive.

    >>> is_field_contains_text(driver=myWebDriver.webdriver,field={"type":"id","value":"lab-name"}, text="your name:")
    True

### The field contains the text in the value attribute

    >>> is_field_contains_text(driver=myWebDriver.webdriver,field={"type":"id","value":"email"}, text="Your.mail@he.re")
    True

Insert some text in it

    >>> fill_element(driver=myWebDriver.webdriver,field={"type":"id","value":"email"}, value="my@email.here")
    0

    >>> is_field_contains_text(driver=myWebDriver.webdriver,field={"type":"id","value":"email"}, text="Your.mail@he.re")
    False

    >>> is_field_contains_text(driver=myWebDriver.webdriver,field={"type":"id","value":"email"}, text="my@email.here")
    True

## Assertions

The web driver is mandatory

    >>> is_field_contains_text()
    Traceback (most recent call last):
    ...
    AssertionError: Driver is expected.


## Teardown

    >>> myWebDriver.close()
    0

    >>> myWebDriver = None

    >>> myserver.stop()

    >>> myserver = None
