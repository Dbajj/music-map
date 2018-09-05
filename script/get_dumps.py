from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import sys
import requests
import pdb
import re
import math
def get_latest_link(links):
    """
    links: a list containing tuples (link,year) where link the url and year is
    a string representing the date of the link

    returns: the link corresponding to the latest year
    """

    latest_link = None
    latest_year = 0

    for (link,year) in links:
        if int(year) > int(latest_year):
            latest_link = link
            latest_year = year

    return latest_link


def get_year_link(html_output):
    reg = re.compile('(http[s]?:\/\/data\.discogs\.com\/.*\/(\d*)\/)')
    links = re.findall(reg,html_output)

    if len(links) == 0:
        raise ValueError('No valid discogs data links found in \
                given html_output')

    return get_latest_link(links)

def get_download_link(html_output,dl_type):
    reg = re.compile(f'((?:http)?[s]?:?\/\/discogs-data\..*\/data\/\d*\/discogs_(\d*)_{dl_type}\.xml\.gz)')

    links = re.findall(reg,html_output)

    if len(links) == 0:
        raise ValueError('No valid discogs data links found in \
                given html_output')

    latest = get_latest_link(links)
    if latest.startswith('http:'):
        return latest
    else:
        return 'http:' + latest


    return get_latest_link(links)

def download_file(link, output_name):
    response = requests.get(link, stream=True)
    response.raise_for_status()
    with open(output_name, 'wb') as f:
        down = 0
        length = int(response.headers.get('content-length'))
        for block in response.iter_content(1024*1024*5):
            down += len(block)
            done = int(50 * down / length )
            sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
            sys.stdout.flush()
            f.write(block)
        print(f"\nFile saved as \"{output_name}\"")







# Setup selenium headless driver with options
options = Options()
options.set_headless(headless=True)
driver = webdriver.Chrome(chrome_options=options)
driver.implicitly_wait(2)

# Connect to the data dump landing page
driver.get('http://data.discogs.com')
wait = WebDriverWait(driver,10)
wait.until(expected_conditions.presence_of_element_located((By.ID,'listing')))
assert 'Discogs Data' in driver.title

# Grab the link for the latest year dump
year_link = get_year_link(driver.page_source)
driver.get(year_link)
wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,'#listing a')))

# Download latest artist dump
latest = get_download_link(driver.page_source,'artists')
print("Downloading artist dump from " + latest)
download_file(latest,'artists.xml.gz')

# Download latest master dump
latest = get_download_link(driver.page_source,'masters')
print("Downloading masters dump from " + latest)
download_file(latest,'masters.xml.gz')

# Download latest releases dump
latest = get_download_link(driver.page_source,'releases')
print("Downloading releases dump from " + latest)
download_file(latest,'releases.xml.gz')




