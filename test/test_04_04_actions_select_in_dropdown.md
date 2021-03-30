# eaiautomatontools.actions.set_checkbox

Present the action utilities for Selenium automaton.
The set_checkbox method will update the status of the checkbox to match the expected one.

## Background

Launch a test web server serving controlled web pages on localhost port 8081

Use the python resources server.

    >>> from eaiautomatontools.resources.server import TestServer

    >>> myserver = TestServer()

    >>> myserver.start()

Instantiate a web driver using the eaiautomatontools.browserServer

    >>> from eaiautomatontools.browserServer import BrowserServer

    >>> myWebDriver = BrowserServer()

Use a default browser such as Chrome in 32 bit version

    >>> myWebDriver.browser_name = "chrome"

Serve the web driver

    >>> myWebDriver.serve()
    <BLANKLINE>
    <BLANKLINE>
    0

Open the form test page

    >>> myWebDriver.go_to("http://127.0.0.1:8081/select.html")
    0

Import the find_element tool

    >>> from eaiautomatontools.finders import find_element

    >>> from selenium.webdriver.support.select import Select

Import the set_checkbox tool

    >>> from eaiautomatontools.actions import select_in_dropdown

## Nominal case: all fields are valid

    >>> select_in_dropdown(driver=myWebDriver.webdriver, field={'type':'id','value':'county'},visible_text="County Kilkenny")
    0

    >>> mySelect = Select(find_element(driver=myWebDriver.webdriver, field={'type':'id','value':'county'}))

    >>> ["value: '{}' visible text: '{}'".format(element.get_attribute("value"), element.text) for element in mySelect.all_selected_options]
    ["value: 'Kilkenny' visible text: 'County Kilkenny'"]

    >>> select_in_dropdown(driver=myWebDriver.webdriver, field={'type':'id','value':'county'},value="Meath")
    0

    >>> ["value: '{}' visible text: '{}'".format(element.get_attribute("value"), element.text) for element in mySelect.all_selected_options]
    ["value: 'Meath' visible text: 'County Meath'"]


## Assertion errors

### The web driver is not given.

    >>> select_in_dropdown(field={'type':'id','value':'county'},value="Meath")
    Traceback (most recent call last):
    ...
    AssertionError: Driver is expected.

### The field is not valid

#### The keys are not one of "type" or "value"

    >>> select_in_dropdown(driver=myWebDriver.webdriver, field={'type':'id','val':'county'},value="Meath")
    Traceback (most recent call last):
    ...
    AssertionError: Field '{'type': 'id', 'val': 'county'}' is not a valid field

#### Incorrect type key value not in

    >>> select_in_dropdown(driver=myWebDriver.webdriver, field={'type':'if','value':'county'},visible_text="County Kilkenny")
    Traceback (most recent call last):
    ...
    AssertionError: Field '{'type': 'if', 'value': 'county'}' is not a valid field

## Exception errors

### The element can't be found

    >>> select_in_dropdown(driver=myWebDriver.webdriver, field={'type':'id','value':'lander'},value="Meath")
    Traceback (most recent call last):
     ...
    selenium.common.exceptions.NoSuchElementException: Message: Element designed by field '{'type': 'id', 'value': 'lander'}' could not be located.
    <BLANKLINE>

### The option can't be located

    >>> select_in_dropdown(driver=myWebDriver.webdriver, field={'type':'id','value':'county'},value="toto")
    Traceback (most recent call last):
     ...
    selenium.common.exceptions.NoSuchElementException: Message: Cannot locate option with value: toto
    <BLANKLINE>

### Not a drop down

    >>> select_in_dropdown(driver=myWebDriver.webdriver, field={'type':'id','value':'myDiv'},value="Meath")
    Traceback (most recent call last):
    ...
    Exception: Select only works on <select> elements, not on <div>

## Teardown

    >>> myWebDriver.close()
    0

    >>> myWebDriver = None

    >>> myserver.stop()

    >>> myserver = None