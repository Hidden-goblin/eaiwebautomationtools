# eaiautomatontools.finders.find_from_elements

Present the finder utilities for Selenium automaton.
The find_from_elements method try to locate an element from a list with its text.

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

    >>> from eaiautomatontools.finders import find_from_elements

If the page contains multiple elements it will select the right one.

    >>> myElement = find_from_elements(driver=myWebDriver.webdriver,field={"type":"tag_name","value":"a"},text="second page")

    >>> type(myElement)
    <class 'selenium.webdriver.remote.webelement.WebElement'>

    >>> myElement.text
    'second page'

If the page contains only one element it will select this element. However you may look at the find_element which should be faster.

    >>> myElement = find_from_elements(driver=myWebDriver.webdriver,field={"type":"id","value":"tables"},text="tables test page")

    >>> type(myElement)
    <class 'selenium.webdriver.remote.webelement.WebElement'>

    >>> myElement.text
    'tables test page'

## Not found element

    >>> myElement = find_from_elements(driver=myWebDriver.webdriver,field={"type":"tag_name","value":"a"},text="page")
    
    >>> type(myElement)
    <class 'NoneType'>

## The web driver is mandatory

    >>> myElement = find_from_elements(field={"type":"xpath","value":"html/body/div[2]"})
    Traceback (most recent call last):
    ...
    TypeError: Driver is expected

## The field must be a dictionary with type and value key
    
    >>> myElement = find_from_elements(driver=myWebDriver.webdriver, text="tables test page")
    Traceback (most recent call last):
    ...
    TypeError: None is not a dictionary

    >>> myElement = find_from_elements(driver=myWebDriver.webdriver,field={"value":"tables"},text="tables test page")
    Traceback (most recent call last):
    ...
    KeyError: "The field argument doesn't contains either the 'type' or 'value' key."

    >>> myElement = find_from_elements(driver=myWebDriver.webdriver,field={"type":"id"},text="tables test page")
    Traceback (most recent call last):
    ...
    KeyError: "The field argument doesn't contains either the 'type' or 'value' key."

    

## The text value must be a non-empty string

    >>> myElement = find_from_elements(driver=myWebDriver.webdriver,field={"type":"id","value":"tables"})
    Traceback (most recent call last):
    ...
    AttributeError: text must be provided

    >>> myElement = find_from_elements(driver=myWebDriver.webdriver,field={"type":"id","value":"tables"},text=3)
    Traceback (most recent call last):
    ...
    AttributeError: text must be a string

    >>> myElement = find_from_elements(driver=myWebDriver.webdriver,field={"type":"id","value":"tables"},text="")
    Traceback (most recent call last):
    ...
    ValueError: text must be non-empty

## TearDown

Close all windows

    >>> myWebDriver.close()
    0

Stop the web server

    >>> myserver.stop()
