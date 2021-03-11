# eaiautomatontools.navigators.go_to_window

Present the navigators utilities for Selenium automaton.
This document will only present the go_to_window function


# Background

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

Request the test page resources/popups.html

    >>> myWebDriver.go_to("http://127.0.0.1:8081/popups.html")
    0

Use the finders tools in order to retrieve link elements within the page

    >>> from eaiautomatontools.finders import find_from_elements, find_element


# Switch to window

Use the navigators tools

    >>> from eaiautomatontools.navigators import go_to_window

# Can't switch to window with the same page title

Open two windows with the same page title

    >>> find_from_elements(driver=myWebDriver.webdriver,field={"type":"tag_name","value":"a"}, text="Use target").click()
    ...

    >>> find_from_elements(driver=myWebDriver.webdriver,field={"type":"tag_name","value":"a"}, text="Use JS with default").click()
    ...

Switch now to the window with the "My default pop up" title.

    >>> go_to_window(driver=myWebDriver.webdriver, title="My default pop up")
    Traceback (most recent call last):
    ...
    Exception: Too many windows with the same title to switch to. Staying on the current window.

It raises an Exception because the

Now clean the browser and reopen the first page only

    >>> myWebDriver.close()
    0

    >>> myWebDriver.serve()
    <BLANKLINE>
    <BLANKLINE>
    0

    >>> myWebDriver.go_to("http://127.0.0.1:8081/popups.html")
    0

# Switch to window with the page title when each pages have different title

Current page title is

    >>> myWebDriver.webdriver.title
    'Pop ups test page'

    >>> find_from_elements(driver=myWebDriver.webdriver,field={"type":"tag_name","value":"a"}, text="Use target").click()
    ...

    >>> find_from_elements(driver=myWebDriver.webdriver,field={"type":"tag_name","value":"a"}, text="Use JS with first").click()
    ...

    >>> go_to_window(driver=myWebDriver.webdriver, title="My default pop up")
    0

    >>> myWebDriver.webdriver.title
    'My default pop up'

Search for the body text

    >>> element = find_element(driver=myWebDriver.webdriver, field={"type":"tag_name", "value":"body"})

    >>> element.text
    'A little sad story with bright sentences.'

Switch to another window

    >>> go_to_window(driver=myWebDriver.webdriver, title="My pop up")
    0

    >>> myWebDriver.webdriver.title
    'My pop up'

Now clean the browser and reopen the first page only

    >>> myWebDriver.close()
    0

    >>> myWebDriver.serve()
    <BLANKLINE>
    <BLANKLINE>
    0

    >>> myWebDriver.go_to("http://127.0.0.1:8081/popups.html")
    0

# Switch to window using the window handles

Current page handle is

    >>> current_handle = myWebDriver.webdriver.current_window_handle

Open popups

    >>> find_from_elements(driver=myWebDriver.webdriver,field={"type":"tag_name","value":"a"}, text="Use target").click()
    ...

    >>> find_from_elements(driver=myWebDriver.webdriver,field={"type":"tag_name","value":"a"}, text="Use JS with default").click()
    ...

Get all handles

    >>> handles = myWebDriver.webdriver.window_handles

We must see three handles, one per window

    >>> len(handles)
    3

Get all windows page title

    >>> for handle in handles:
    ...     go_to_window(driver=myWebDriver.webdriver,handle=handle)
    ...     print(myWebDriver.webdriver.title)
    0
    Pop ups test page
    0
    My default pop up
    0
    My default pop up


## Teardown

    >>> myWebDriver.close()
    0

    >>> myserver.stop()
