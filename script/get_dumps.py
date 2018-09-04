from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
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



options = Options()
options.set_headless(headless=True)
driver = webdriver.Chrome(chrome_options=options)
driver.implicitly_wait(2)
driver.get('http://data.discogs.com')
wait = WebDriverWait(driver,10)
wait.until(expected_conditions.presence_of_element_located((By.ID,'listing')))
assert 'Discogs Data' in driver.title

year_link = get_year_link(driver.page_source)
driver.get(year_link)
wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,'#listing a')))

latest = get_download_link(driver.page_source,'artists')
