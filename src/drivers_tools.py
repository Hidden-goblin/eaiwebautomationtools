# -*- coding: utf-8 -*-
import logging
from os import remove
from time import sleep

from PIL import Image
from selenium import webdriver

log = logging.getLogger(__name__)


def web_drivers_tuple():
    return (webdriver.firefox.webdriver.WebDriver,
            webdriver.chrome.webdriver.WebDriver,
            webdriver.ie.webdriver.WebDriver,
            webdriver.edge.webdriver.WebDriver)


def fullpage_screenshot(driver, file):
    log.debug("Starting full page screenshot")
    total_width = driver.execute_script("return document.body.offsetWidth")
    total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    viewport_width = driver.execute_script("return document.body.clientWidth")
    viewport_height = driver.execute_script("return window.innerHeight")
    log.debug("Total: ({0}, {1}), Viewport: ({2},{3})".format(total_width, total_height,
                                                              viewport_width, viewport_height))
    rectangles = []
    i = 0
    while i < total_height:
        ii = 0
        top_height = i + viewport_height

        if top_height > total_height:
            top_height = total_height

        while ii < total_width:
            top_width = ii + viewport_width

            if top_width > total_width:
                top_width = total_width

            log.debug("Appending rectangle ({0},{1},{2},{3})".format(ii, i, top_width, top_height))
            rectangles.append((ii, i, top_width, top_height))
            ii = ii + viewport_width
        i = i + viewport_height
    stitched_image = Image.new('RGB', (total_width, total_height))
    previous = None
    part = 0
    for rectangle in rectangles:
        if previous is not None:
            driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
            log.debug("Scrolled To ({0},{1})".format(rectangle[0], rectangle[1]))
            sleep(0.2)
        file_name = "part_{0}.png".format(part)
        log.debug("Capturing {0} ...".format(file_name))
        driver.get_screenshot_as_file(file_name)
        screenshot = Image.open(file_name)
        if rectangle[1] + viewport_height > total_height:
            offset = (rectangle[0], total_height - viewport_height)
        else:
            offset = (rectangle[0], rectangle[1])
        log.debug("Adding to stitched image with offset ({0}, {1})".format(offset[0], offset[1]))
        stitched_image.paste(screenshot, offset)
        del screenshot
        remove(file_name)
        part = part + 1
        previous = rectangle
    try:
        stitched_image.save(file)
    except IOError:
        return False
    log.info("Screenshot saved: {}".format(file))
    return True
