# eaiautomatontools.finders.find_element

Present the finder utilities for Selenium automaton.

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

Request the web server IP 127.0.0.1:8081

    >>> myWebDriver.go_to("http://localhost:8081")
    ...
    0

## Find an element

    >>> from eaiautomatontools.finders import find_element

### Find by id

    >>> myElement = find_element(driver=myWebDriver.webdriver, field={"type":"id","value":"first"})

    >>> myElement.tag_name
    'div'

    >>> myElement.text
    'A text here with a link to a second page'

    >>> myElement.is_displayed()
    True

    >>> myElement.is_enabled()
    True

    >>> myElement.is_selected()
    False

### Find by name

    >>> myElement = find_element(driver=myWebDriver.webdriver, field={"type":"name","value":"test-div"})

    >>> type(myElement)
    <class 'selenium.webdriver.remote.webelement.WebElement'>

    >>> myElement.text
    'The tables test page'

### Find by tag_name

    >>> myElement = find_element(driver=myWebDriver.webdriver, field={"type":"tag_name","value":"a"})

    >>> type(myElement)
    <class 'selenium.webdriver.remote.webelement.WebElement'>

It will return the first tag found.

    >>> myElement.text
    'second page'

### Find by link_text

    >>> myElement = find_element(driver=myWebDriver.webdriver, field={"type":"link_text","value":"second page"})

    >>> type(myElement)
    <class 'selenium.webdriver.remote.webelement.WebElement'>

    >>> myElement.text
    'second page'

### Find by partial_link_text

    >>> myElement = find_element(driver=myWebDriver.webdriver, field={"type":"partial_link_text","value":"second"})

    >>> type(myElement)
    <class 'selenium.webdriver.remote.webelement.WebElement'>

    >>> myElement.text
    'second page'

### Find by css

    >>> myElement = find_element(driver=myWebDriver.webdriver, field={"type":"css","value":"div"})

    >>> type(myElement)
    <class 'selenium.webdriver.remote.webelement.WebElement'>

It will return the first element found;

    >>> myElement.text
    'A text here with a link to a second page'

Another example

    >>> myElement = find_element(driver=myWebDriver.webdriver, field={"type":"css","value":"a#tables"})

    >>> myElement.text
    'tables test page'

### Find by xpath

    >>> myElement = find_element(driver=myWebDriver.webdriver, field={"type":"xpath","value":"html/body/div[2]"})

    >>> type(myElement)
    <class 'selenium.webdriver.remote.webelement.WebElement'>

    >>> myElement.text
    'The tables test page'

### Find an element giving a text value

    >>> myWebDriver.go_to("http://localhost:8081/forms.html")
    ...
    0

    >>> myElement = find_element(driver=myWebDriver.webdriver, field={"type":"tag_name","value":"input", "text": "Your.mail@he.re"})

    >>> myElement.get_attribute("value")
    'Your.mail@he.re'

## Not found element

    >>> myWebDriver.go_to("http://localhost:8081")
    ...
    0

    >>> myElement = find_element(driver=myWebDriver.webdriver, field={"type":"id","value":"toto"})
    Traceback (most recent call last):
    ...
    selenium.common.exceptions.NoSuchElementException: Message: Element designed by field '{'type': 'id', 'value': 'toto'}' could not be located.
    <BLANKLINE>

    >>> myElement = find_element(driver=myWebDriver.webdriver, field={"type":"name","value":"toto-div"})
    Traceback (most recent call last):
    ...
    selenium.common.exceptions.NoSuchElementException: Message: Element designed by field '{'type': 'name', 'value': 'toto-div'}' could not be located.
    <BLANKLINE>

    >>> myElement = find_element(driver=myWebDriver.webdriver, field={"type":"tag_name","value":"table"})
    Traceback (most recent call last):
    ...
    selenium.common.exceptions.NoSuchElementException: Message: Element designed by field '{'type': 'tag_name', 'value': 'table'}' could not be located.
    <BLANKLINE>

    >>> myElement = find_element(driver=myWebDriver.webdriver, field={"type":"link_text","value":"toto page"})
    Traceback (most recent call last):
    ...
    selenium.common.exceptions.NoSuchElementException: Message: Element designed by field '{'type': 'link_text', 'value': 'toto page'}' could not be located.
    <BLANKLINE>

    >>> myElement = find_element(driver=myWebDriver.webdriver, field={"type":"partial_link_text","value":"toto"})
    Traceback (most recent call last):
    ...
    selenium.common.exceptions.NoSuchElementException: Message: Element designed by field '{'type': 'partial_link_text', 'value': 'toto'}' could not be located.
    <BLANKLINE>

    >>> myElement = find_element(driver=myWebDriver.webdriver, field={"type":"css","value":"input"})
    Traceback (most recent call last):
    ...
    selenium.common.exceptions.NoSuchElementException: Message: Element designed by field '{'type': 'css', 'value': 'input'}' could not be located.
    <BLANKLINE>

    >>> myElement = find_element(driver=myWebDriver.webdriver, field={"type":"xpath","value":"html/body/span"})
    Traceback (most recent call last):
    ...
    selenium.common.exceptions.NoSuchElementException: Message: Element designed by field '{'type': 'xpath', 'value': 'html/body/span'}' could not be located.
    <BLANKLINE>

## The web driver is mandatory

    >>> myElement = find_element(field={"type":"xpath","value":"html/body/div[2]"})
    Traceback (most recent call last):
    ...
    TypeError: Driver is expected

## The field value is mandatory

    >>> myElement = find_element(driver=myWebDriver.webdriver)
    Traceback (most recent call last):
    ...
    TypeError: None is not a dictionary

## The field value must contains a type and a value key

    >>> myElement = find_element(driver=myWebDriver.webdriver, field={"type":"xpath"})
    Traceback (most recent call last):
    ...
    KeyError: "The field argument doesn't contains either the 'type' or 'value' key."

    >>> myElement = find_element(driver=myWebDriver.webdriver, field={"value":"html/body/span"})
    Traceback (most recent call last):
    ...
    KeyError: "The field argument doesn't contains either the 'type' or 'value' key."

## The field key `type` value must be one of a limited list

`type` must be in a limited list of values:

* id: when you want to retrieve the field by its id
* name: when you want to retrieve the field by its name attribute's value
* class_name: when you want to retrieve the field by one of its class value
* link_text: when you want to retrieve the field by the exact match on the link text
* partial_link_text: when you want to retrieve the field by a sub string of the link text
* css: when you want to retrieve the field by its css path
* xpath: when you want to retrieve the field by its xpath
* tag_name: when you want to retrieve the field by its tag name



    >>> myElement = find_element(driver=myWebDriver.webdriver, field={"type":"test", "value": "test"})
    Traceback (most recent call last):
    ...
    ValueError: The field type is not one the expected: '('id', 'name', 'class_name', 'link_text', 'css', 'partial_link_text', 'xpath', 'tag_name')

    
TearDown
-------------------------
Close all windows

    >>> myWebDriver.close()
    0

Stop the web server

    >>> myserver.stop()
