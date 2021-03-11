# eaiautomatontools.take_a_screenshot

Present the screenshot utility for Selenium automaton.

The take_a_screenshot is a selenium web driver function.

Screenshot could be full page or partial.

## Initialise browserServer & resources server

Use the python resources server.

    >>> from eaiautomatontools.resources.server import TestServer

    >>> myserver = TestServer()

    >>> myserver.start()

Instantiate a web driver using the eaiautomatontools.browserServer

    >>> from eaiautomatontools.browserServer import BrowserServer

    >>> myBrowser = BrowserServer()

    >>> myBrowser.browser_name = "Chrome"
    
    >>> myBrowser.serve()
    <BLANKLINE>
    <BLANKLINE>
    0

    >>> myBrowser.go_to(url="http://127.0.0.1:8081/screenshot.html")
    0

## Screenshots

You can ask the browserServer to take a screenshot of the current page and save to somewhere. By default it's in your
temporary folder under automaton_screenshots/screenshot-<millisecond timestamp>.png file and will take the full page
not only the displayed part.

    >>> myBrowser.take_a_screenshot()
    0

You can specify the folder you want to save the file to. The path should be valid and accessible.

    >>> myBrowser.take_a_screenshot(save_to="toto/")
    Traceback (most recent call last):
    ...
    OSError: The screenshot could not be done. Please check if the file path is correct. Get 'False'

Please note the temp folder is cleaned as soon as you recreate a new BrowserServer object.

# Screenshots full page

You can choose to take a screenshot of a full page or partial. By default the full page will be used.

    >>> myBrowser.take_a_screenshot(save_to="test/")
    0

Import glob for easy file list.

    >>> import glob

Retrieve the file list in a list :-)

    >>> screenshot_list = glob.glob("test/screenshot-*.png")

As we've done only one screenshot, the list length is only one.

    >>> len(screenshot_list)
    1

Remove the screenshot (it's cleaner isn't it?)

    >>> import os

    >>> os.remove(screenshot_list[0])

You can specify you want full page screenshot too

    >>> myBrowser.take_a_screenshot(save_to="test/", is_full_screen=True)
    0

    >>> screenshot_list = glob.glob("test/screenshot-*.png")

    >>> os.remove(screenshot_list[0])

If the option is_full_screen (accepted boolean: 'True' or 'False') is not valid, the default value will be 'True'

    >>> myBrowser.take_a_screenshot(save_to="test/", is_full_screen='bad value')
    0

Check the screenshot dimension and delete it.

    >>> from PIL import Image

    >>> screenshot_list = glob.glob("test/screenshot-*.png")

The screenshot resolution is: width= 800px and height=1824px

    >>> print( Image.open(screenshot_list[0]).size)
    (950, 1824)

    >>> os.remove(screenshot_list[0])

# Screenshots partial

To only take a partial screenshot, who will save the displayed frame you need to specify it with the
option full_screen in take_a_screenshot. This function used selenium webdriver code.

    >>> myBrowser.take_a_screenshot(save_to="test/", is_full_screen=False)
    0

Check the screenshot dimension and remove it.

    >>> from PIL import Image

    >>> screenshot_list = glob.glob("test/screenshot-*.png")

The screenshot resolution is: width= 95px and height=1824px

    >>> print( Image.open(screenshot_list[0]).size)
    (1295, 843)

    >>> os.remove(screenshot_list[0])

# Teardown

    >>> myBrowser.close()
    0

    >>> myBrowser = None

    >>> myserver.stop()

    >>> myserver = None
