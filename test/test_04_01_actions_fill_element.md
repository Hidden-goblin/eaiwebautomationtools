# eaiautomatontools.actions.fill_element

Present the action utilities for Selenium automaton.
The fill_element method try to locate an element and fill it with the value. We assume the element can receive a text.
It will raise an exception if it's not the case.

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

Import the find_element tool

    >>> from eaiautomatontools.finders import find_element

Import the fill_element tool

    >>> from eaiautomatontools.actions import fill_element



## Nominal case: give a web driver, give a valid field

Retrieve the name input textfield.

    >>> myElement = find_element(driver=myWebDriver.webdriver, field={"type":"id","value":"name"})


Look at its value. It's empty.

    >>> myElement.get_attribute("value")
    ''

Fill the textfield with the value "my name"

    >>> fill_element(driver=myWebDriver.webdriver, field={"type":"id", "value":"name"},value="my name")
    0

Check the textfield has been updated.

    >>> myElement = find_element(driver=myWebDriver.webdriver, field={"type":"id","value":"name"})

    >>> myElement.get_attribute("value")
    'my name'


## Assertion cases

### The web driver is missing.

    >>> fill_element(field={"type":"id", "value":"name"},value="my name")
    Traceback (most recent call last):
    ...
    TypeError: Driver is expected

### The field is not valid.

#### Incorrect type key value.

    >>> fill_element(driver=myWebDriver.webdriver, field={"type":"idl", "value":"name"},value="my name")
    Traceback (most recent call last):
    ...
    ValueError: The field type is not one the expected: '('id', 'name', 'class_name', 'link_text', 'css', 'partial_link_text', 'xpath', 'tag_name')

### Incorrect keys value.

    >>> fill_element(driver=myWebDriver.webdriver, field={"typ":"id", "value":"name"},value="my name")
    Traceback (most recent call last):
    ...
    KeyError: "The field argument doesn't contains either the 'type' or 'value' key."

    >>> fill_element(driver=myWebDriver.webdriver, field={"type":"id", "val":"name"},value="my name")
    Traceback (most recent call last):
    ...
    KeyError: "The field argument doesn't contains either the 'type' or 'value' key."


## Exception case

The element is not user editable

    >>> fill_element(driver=myWebDriver.webdriver, field={"type":"id", "value":"lab-name"},value="my name")
    1

The element can't be found

    >>> fill_element(driver=myWebDriver.webdriver, field={"type":"id", "value":"lab-nam"},value="my name")
    1

## Teardown
------------------------------
    >>> myWebDriver.close()
    0

    >>> myWebDriver = None

    >>> myserver.stop()

    >>> myserver = None
