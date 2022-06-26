# eaiautomatontools.information.retrieve_tabular

Present the information utilities for Selenium automaton.

Return the table data as a list of lists.


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
  
  

Open the popups test page

    >>> myWebDriver.go_to("http://localhost:8081/tables.html")
    0

## Nominal case

Import the information tool

    >>> from eaiautomatontools.information import retrieve_tabular

We will retrieve the first tabular in the page using the xpath locator and save the data into a `tab` variable

    >>> tab = retrieve_tabular(myWebDriver.webdriver, {"type": "xpath", "value": "/html/body/table[1]"})
    >>> tab
    [['First name', 'Last name'], ['John', 'Doe'], ['Jane', 'Doe']]

It works based on the `tr` and `td` tags. 
    
    >>> tab2 = retrieve_tabular(myWebDriver.webdriver, {"type": "xpath", "value": "/html/body/table[2]"})
    >>> tab2
    [['Header content 1', 'Header content 2'], ['Body content 1', 'Body content 2'], ['Footer content 1', 'Footer content 2']]

And it's case-insensitive

    >>> tab3 = retrieve_tabular(myWebDriver.webdriver, {"type": "xpath", "value": "/html/body/table[1]"}, row_and_col=('TR', 'TD', 'TH'))
    >>> tab3
    [['First name', 'Last name'], ['John', 'Doe'], ['Jane', 'Doe']]

## Error cases

### Row and col tags are not found
    >>> tab = retrieve_tabular(myWebDriver.webdriver, {"type": "xpath", "value": "/html/body/table[1]"}, row_and_col=('XR', 'XD', 'XH'))
    >>> tab
    []

### Table not found
    >>> tab = retrieve_tabular(myWebDriver.webdriver, {"type": "xpath", "value": "/html/body/table[7]"})
    
    >>> type(tab)
    <class 'NoneType'>

## Teardown

    >>> myWebDriver.close()
    0

    >>> myWebDriver = None

    >>> myserver.stop()

    >>> myserver = None
