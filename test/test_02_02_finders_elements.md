# eaiautomatontools.finders.find_elements

Present the finder utilities for Selenium automaton.


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

Request the web server IP 127.0.0.1:8081

    >>> myWebDriver.go_to("http://127.0.0.1:8081")
    ...
    0

## Find an element
--------------------------
    >>> from eaiautomatontools.finders import find_elements

### Find by id
    >>> myElements = find_elements(driver=myWebDriver.webdriver, field={"type":"id","value":"first"})

    >>> len(myElements)
    1

    >>> type(myElements[0])
    <class 'selenium.webdriver.remote.webelement.WebElement'>

    >>> myElements[0].text
    'A text here with a link to a second page'

### Find by name
    >>> myElements = find_elements(driver=myWebDriver.webdriver, field={"type":"name","value":"test-div"})

    >>> len(myElements)
    1

    >>> type(myElements[0])
    <class 'selenium.webdriver.remote.webelement.WebElement'>

    >>> myElements[0].text
    'The tables test page'

### Find by tag_name
    >>> myElements = find_elements(driver=myWebDriver.webdriver, field={"type":"tag_name","value":"a"})

    >>> len(myElements)
    2

    >>> [type(elem) for elem in myElements]
    [<class 'selenium.webdriver.remote.webelement.WebElement'>, <class 'selenium.webdriver.remote.webelement.WebElement'>]

    >>> [elem.text for elem in myElements]
    ['second page', 'tables test page']

### Find by link_text
    >>> myElements = find_elements(driver=myWebDriver.webdriver, field={"type":"link_text","value":"second page"})

    >>> len(myElements)
    1

    >>> type(myElements[0])
    <class 'selenium.webdriver.remote.webelement.WebElement'>

    >>> myElements[0].text
    'second page'

### Find by partial_link_text
    >>> myElements = find_elements(driver=myWebDriver.webdriver, field={"type":"partial_link_text","value":"page"})

    >>> len(myElements)
    2

    >>> [type(elem) for elem in myElements]
    [<class 'selenium.webdriver.remote.webelement.WebElement'>, <class 'selenium.webdriver.remote.webelement.WebElement'>]

    >>> [elem.text for elem in myElements]
    ['second page', 'tables test page']

### Find by css
    >>> myElements = find_elements(driver=myWebDriver.webdriver, field={"type":"css","value":"div"})

    >>> len(myElements)
    3

    >>> [type(elem) for elem in myElements]
    [<class 'selenium.webdriver.remote.webelement.WebElement'>, <class 'selenium.webdriver.remote.webelement.WebElement'>, <class 'selenium.webdriver.remote.webelement.WebElement'>]

    >>> [elem.text for elem in myElements]
    ['A text here with a link to a second page', 'The tables test page', '']

### Find by xpath
    >>> myElements = find_elements(driver=myWebDriver.webdriver, field={"type":"xpath","value":"html/body/div"})

    >>> len(myElements)
    3

    >>> [type(elem) for elem in myElements]
    [<class 'selenium.webdriver.remote.webelement.WebElement'>, <class 'selenium.webdriver.remote.webelement.WebElement'>, <class 'selenium.webdriver.remote.webelement.WebElement'>]

    >>> [elem.text for elem in myElements]
    ['A text here with a link to a second page', 'The tables test page', '']


### Not found element

    >>> myElements = find_elements(driver=myWebDriver.webdriver, field={"type":"id","value":"toto"})

    >>> len(myElements)
    0

    >>> myElements = find_elements(driver=myWebDriver.webdriver, field={"type":"name","value":"toto-div"})

    >>> len(myElements)
    0

    >>> myElements = find_elements(driver=myWebDriver.webdriver, field={"type":"tag_name","value":"input"})

    >>> len(myElements)
    0

    >>> myElements = find_elements(driver=myWebDriver.webdriver, field={"type":"link_text","value":"toto page"})

    >>> len(myElements)
    0

    >>> myElements = find_elements(driver=myWebDriver.webdriver, field={"type":"partial_link_text","value":"toto"})

    >>> len(myElements)
    0

    >>> myElements = find_elements(driver=myWebDriver.webdriver, field={"type":"css","value":"input"})

    >>> len(myElements)
    0

    >>> myElements = find_elements(driver=myWebDriver.webdriver, field={"type":"xpath","value":"html/body/input"})

    >>> len(myElements)
    0

## The web driver is mandatory

    >>> myElements = find_elements(field={"type":"xpath","value":"html/body/div[2]"})
    Traceback (most recent call last):
    ...
    AssertionError: Driver is expected.

## Field is mandatory

    >>> myElements = find_elements(driver=myWebDriver.webdriver)
    Traceback (most recent call last):
    ...
    AssertionError: Field must be a dictionary

## Field type and value key are mandatory
    >>> myElements = find_elements(driver=myWebDriver.webdriver, field={"value":"html/body/input"})
    Traceback (most recent call last):
    ...
    KeyError: KeyError("The field argument doesn't contains either the 'type' or 'value' key.")

    >>> myElements = find_elements(driver=myWebDriver.webdriver, field={"type":"xpath"})
    Traceback (most recent call last):
    ...
    KeyError: KeyError("The field argument doesn't contains either the 'type' or 'value' key.")

## TearDown

Close all windows

    >>> myWebDriver.close()
    0

Stop the web server

    >>> myserver.stop()
