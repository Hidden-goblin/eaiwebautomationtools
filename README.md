Automaton Tools module
======================

The automaton tools module provide an abstraction of the selenium web driver through a "BrowserServer" object.

Note on documentation
=====================

The documentation is build upon the doctest's files. It includes some weird sections such as "Teardown" 
section: Don't be afraid is testing part ;)

Documentation is on [ReadTheDocs](https://eaiwebautomationtools.readthedocs.io)

System requirements
===================

This module has been developed with Python 3.7 and uses selenium version 3.14.

All code is accessible on [GitHub](https://github.com/Hidden-goblin/eaiwebautomationtools)

BrowserServer object
=====================

The BrowserServer is packaged with the webdriver-manager. You can require:

- chrome
- headless-chrome
- firefox
- edge
- opera
- safari (it's not managed by webdriver-manager: you have to provide the path to the webdriver)


Serve the webdriver
-------------------

When everything is set you can call "serve()" method which open the browser of the specified type.

You can stop the webdriver by invoking the "close()" method.

Interacting with the browser
============================

The main feature is unifying the way you choose to interact with the browser.

An element is described by a dictionary in which we give a type and a value.

The **type** is one of the following:

-   id: the element identifier,
-   name: the element name,
-   class\_name: the element class name,
-   css: the element css path,
-   link\_text: the link full text,
-   partial\_link\_text: the link partial text,
-   tag\_name: the element tag name
-   xpath: the element xpath



The **value** contains the actual value for the **type**. For example an element with the "id" type must have  
the id's value to be correctly defined. In the same way an element with the "tag_name" type and a value "div" may return all div on the web page.

To avoid, as much as possible, this multi-definition you can add a **text** dictionary key which try to locate the element with this exact text. **You may find an element with an empty text so use it with care.**

Although the BrowserServer class is a must have, you can use the module spaces separately. I will quickly present here only the BrowserServer class method but the module spaces functions only add a "driver" attribute which hold the selemium web driver to use.

finders
-------

This module space is about finding and returning web element.

-   find\_element(field,\[web_element\]): return the first element which match the criteria. Use the web_element as base element in order to find nested element. 
-   find\_elements(field, \[web_element\]): return all elements which match the criteria in a list. Use the web_element as base element in order to find nested element.
-   find\_from\_elements(field,text, \[web_element\]): return the first element which match the criteria and has the text. Use the web_element as base element in order to find nested element.

information
-----------

This module space is about retrieving data from the web page or the browser.

-   is\_field\_exist(field,until): return the first element which match the criteria within "until" second. Return None otherwise.
-   is\_field\_contains\_text(field,text): return true if the field contains the text even in the value, false otherwise.
-   is\_alert\_present(until): return true if an alert is present within "until" second.
-   element\_text(field): return the field text.
-   how\_many\_windows(): return the number of opened windows.
-   is\_field\_displayed(field): return true if the field is displayed.
-   is\_field\_enabled(field): return true if the field is enabled.

navigators
----------

This module space is about browsing tag and web browsing.

-   go\_to\_url(url): return 0 if successful and go to the specified url.
-   enter\_frame(field): return 0 if successful and enter the page frame/iframe.
-   go\_to\_window(handle,title): return 0 if successful and gain focus on the window defined by its handle ot its title.

alerts
------

This module space is about the alert popups.

- intercept\_alert(messages, accept, value): return 0 if successful. You can specify a list of message which one must be displayed on the alert, accept or reject the alert (Ok or dimiss) and enter a value where the alert prompt for a user input. 
- alert\_message(): return the alert message if an alert is displayed.

actions
-------

This module space is about filling, selecting and clicking on web element.

- fill\_element(field,value): return 0 if successful, fill the field with the value
- fill\_elements(fields, data): return 0 if successful, fill each field in the fields dictionary with the value hold in the data dictionary. You can have a larger fields dictionary than the data but each data entry must be found in the fields dictionary. 
- select\_in\_dropdown(field,visible\_text,value): return 0 if successful, select in the field dropdown the element either described by its visible text or its hidden value. 
- click\_element(field): return 0 if successful, perform a left click on the field.
- mouse\_click(field): return 0 if successful, perform a chain action moving the mouse on the element and mouse click element.
- set\_checked(field,is\_checked): return 0 if successful, set the checkbox field so that the is\_checked value is always true i.e. checked if is\_checked set to true and not checked if is\_checked set to false.

Other documentation
===================

Please find in the test folder doctest files which describe almost all methods here.

Moreover don't hesitate to use the python help(method/class) directly from the python console in order to access the docstring.

To Do
=====

-   Add a multi-selection for dropdown
-   Add a drag & drop functionality
-   Add a get handles functionality

Release Notes
=============
- version 1.0.14:
  - fix missing `web_element` variable in `BrowserServer.set_checkbox` method
  - add `mouse_click` method in the actions
- version 1.0.13:
  - fix missing `avoid_move_to` passing value to find_from_elements when using find_element in conjunction with `text` parameter. 
- version 1.0.12:
    - lower log level for finder(s) actions
    - add wait_for_another_window in information
    - add typing annotations and minimal docstring on BrowserServer
    - fix test_01_01
    - fix case browser_name is None
- version 1.0.11:
    - lower log level for polling actions
- version 1.0.10:
    - add chromium from DriverManager in BrowserServer
- version 1.0.9:
    - actions and finders return None if element not found 
- version 1.0.8:
    - add avoid_move_to option on find_element in order to retrieve an element without moving to it
    - add minor tests
- version 1.0.7:
    - add caller_message to move_to method in order to track down issue in the logs
    - add execute_script method to BrowserServer
    - is_displayed polls every 0.2s for 10s in order to check if field is displayed
    - is_field_exist polls even with StaleElementReferenceException
    - use polling2 instead of webdriver wait where applicable
- version 1.0.6:
    - new test server: now using flask as a test server
    - use mkdocs and the doctest test repository in order to build the documentation
    - add diver option setter
    - add a generic move_to web element method
- version 1.0.5: Sorry for the interruption 
    - use webdriver manager in order to retrieve webdrivers. 
    - Enhance the webdriver handling.
    - Allow providing a WebElement to find nested element(s).
    - Enhance doctest coverage.
    - Minor refactoring
- version 0.1: first release

