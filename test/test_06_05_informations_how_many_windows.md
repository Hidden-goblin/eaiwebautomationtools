# eaiautomatontools.information.how_many_windows

Present the information utilities for Selenium automaton.

Simply return the number of windows currently open.


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
  
  

Open the popups test page

    >>> myWebDriver.go_to("http://localhost:8081/popups.html")
    0

Import the click tool

    >>> from eaiautomatontools.actions import click_element

## Nominal case

Import the information tool

    >>> from eaiautomatontools.information import how_many_windows

Currently, only one window is open

    >>> how_many_windows(myWebDriver.webdriver)
    1

Open a popup

    >>> click_element(myWebDriver.webdriver,{"type": "partial_link_text", "value": "target"})
    0

    >>> how_many_windows(myWebDriver.webdriver)
    2

## Teardown

    >>> myWebDriver.close()
    0

    >>> myWebDriver = None

    >>> myserver.stop()

    >>> myserver = None
