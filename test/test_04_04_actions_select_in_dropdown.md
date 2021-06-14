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

    >>> myWebDriver.go_to("http://localhost:8081/select.html")
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
    TypeError: Driver is expected

### The field is not valid

#### The keys are not one of "type" or "value"

    >>> select_in_dropdown(driver=myWebDriver.webdriver, field={'type':'id','val':'county'},value="Meath")
    Traceback (most recent call last):
    ...
    KeyError: "The field argument doesn't contains either the 'type' or 'value' key."

#### Incorrect type key value not in

    >>> select_in_dropdown(driver=myWebDriver.webdriver, field={'type':'if','value':'county'},visible_text="County Kilkenny")
    Traceback (most recent call last):
    ...
    ValueError: The field type is not one the expected: '('id', 'name', 'class_name', 'link_text', 'css', 'partial_link_text', 'xpath', 'tag_name')

## Exception errors

### The element can't be found

    >>> select_in_dropdown(driver=myWebDriver.webdriver, field={'type':'id','value':'lander'},value="Meath")
    1

### The option can't be located

    >>> select_in_dropdown(driver=myWebDriver.webdriver, field={'type':'id','value':'county'},value="toto")
    1

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
