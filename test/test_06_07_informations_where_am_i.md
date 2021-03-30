# eaiautomatontools.information.retrieve_tabular

Present the information utilities for Selenium automaton.

Return the current url.


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



## Nominal case

Import the information tool

    >>> from eaiautomatontools.information import where_am_i

We will access a page then retrieve the url

    >>> myWebDriver.go_to("http://127.0.0.1:8081/forms.html")
    0
    >>> where_am_i(myWebDriver.webdriver)
    'http://127.0.0.1:8081/forms.html'

## Error cases
It raise a TypeError if the webdriver is not provided as per default the driver is None
    
    >>> where_am_i()
    Traceback (most recent call last):
    ...
    TypeError: Driver is expected as a WebDriver

## Teardown

    >>> myWebDriver.close()
    0

    >>> myWebDriver = None

    >>> myserver.stop()

    >>> myserver = None
