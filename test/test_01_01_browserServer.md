# automatontools.browserServer

Present the browserServer utility for Selenium automaton.

The browserServer is an object which purpose is to serve a selenium web driver.
The object comes with a set of methods.

The constructor will set default attributes. At this stage the browserServer won't be usable.

## Create a browserServer


    >>> from eaiautomatontools.browserServer import BrowserServer

    >>> myBrowser = BrowserServer()

Without settings the server is not usable

    >>> myBrowser.serve()
    Traceback (most recent call last):
    ...
    AttributeError: You must set a browser name. Use one of '['chrome', 'firefox', 'opera', 'edge', 'safari']'

## Setting the browser name
It's quite easy. Use the browser's name you want to control with the limitation of being in the list 'chrome', 'firefox',
'opera', 'edge' and 'safari'.

Please mind that the browser must be installed on your computer.

If you don't you get an error.

    >>> myBrowser.browser_name = 'toto'
    Traceback (most recent call last):
    ...
    ValueError: Unknown browser name. Get toto instead of ['chrome', 'firefox', 'opera', 'edge', 'safari']

Name are not case sensitive

    >>> myBrowser.browser_name = 'ChrOmE'
    >>> myBrowser.browser_name
    'chrome'


At this moment you can serve a selenium web driver

## Serve a web driver

    >>> myBrowser.serve()
    <BLANKLINE>
    <BLANKLINE>
    0

## Get the web driver

    >>> mydriver = myBrowser.webdriver

    >>> type(mydriver)
    <class 'selenium.webdriver.chrome.webdriver.WebDriver'>

## Close a web driver

When closing you discard the web driver. However you can re-serve a new driver at any time.

    >>> myBrowser.close()
    0

    >>> mydriver = myBrowser.webdriver

    >>> type(mydriver)
    <class 'NoneType'>

    >>> myBrowser.serve()
    <BLANKLINE>
    <BLANKLINE>
    0

    >>> mydriver = myBrowser.webdriver

    >>> type(mydriver)
    <class 'selenium.webdriver.chrome.webdriver.WebDriver'>

Go to an URL
----------------------------
From the browserServer object you can do one basic thing navigate to a specific URL.

    >>> myBrowser.go_to(url="http://google.com")
    0

Teardown
------------------------------
    >>> myBrowser.close()
    0

    >>> myBrowser = None
