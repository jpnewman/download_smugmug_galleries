#!/usr/bin/env python

import os
import time
import argparse

from selenium.webdriver import Firefox  # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from urllib2 import urlopen

WEB_PICTURE_SIZE = 'S'  # Small
DOWNLOAD_PICTURE_SIZE = 'O'  # Original

OUTPUT_FOLDER = '_pictures'
IMAGE_PREFIX = 'Pic_'

IMAGE_COUNT = 0
PERVIOUS_IMAGE = ''


def download_image(url):
    """Download from URL."""
    global IMAGE_COUNT

    IMAGE_COUNT += 1

    url_array = url.split('/')
    url = '/'.join(url_array[0:-2]) + '/' + DOWNLOAD_PICTURE_SIZE + '/' + url_array[-1]
    # print(url)

    image_output_filename = '{0:04}{1}'.format(IMAGE_COUNT, os.path.splitext(url)[1])
    image_output_filename = IMAGE_PREFIX + image_output_filename

    image_output_file = os.path.join(OUTPUT_FOLDER, image_output_filename)

    if os.path.isfile(image_output_file):
        print("File already exists and will not be downloaded: {0}".format(image_output_file))
        return

    print("Downloading: {0}".format(image_output_file))

    """Download large binary files."""
    response = urlopen(url)
    CHUNK = 16 * 1024
    with open(image_output_file, 'wb') as f:
        while True:
            chunk = response.read(CHUNK)
            if not chunk:
                break
            f.write(chunk)


def download_all_images(browser):
    """Download Image and Get Next URL."""
    global PERVIOUS_IMAGE

    # Wait for the page to load
    WebDriverWait(browser, timeout=25).until(
        lambda x: x.find_element(By.XPATH, '//button[@data-value="download"]'))

    WebDriverWait(browser, timeout=25).until(
        lambda x: x.find_element(By.XPATH, '//img[@class="sm-lightbox-image"]'))

    image_elem = browser.find_element(By.XPATH, '//img[@class="sm-lightbox-image"]')
    image_src = image_elem.get_attribute('src')
    print(image_src)

    if PERVIOUS_IMAGE == image_src:
        raise "ERROR: Image source not changed: {0}".format(image_src)

    PERVIOUS_IMAGE = image_src

    # NOTE: Double download, once by the browser and once by 'download_url'.
    download_image(image_src)

    next_image = browser.find_element(By.XPATH, '//button[@data-value="right"]')

    if next_image:
        # print(next_image)
        next_image.click()
        time.sleep(5)

        download_all_images(browser)


def _parse_args():
    """Parse Command Arguments."""
    desc = 'Download SmugMug galleries'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('download_url',
                        help='SmugMug galleries URL')

    return parser.parse_args()

def main():
    """Main function."""
    args = _parse_args()

    # Use firefox to get page with javascript generated content
    if not os.path.isdir(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER)

    browser = Firefox()

    try:
        download_url = args.download_url.rstrip('/')
        url = '/'.join([download_url, WEB_PICTURE_SIZE])
        browser.get(url)
        download_all_images(browser)
    finally:
        # browser.quit()
        pass


if __name__ == "__main__":
    main()
