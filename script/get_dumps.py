from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pdb

options = Options()
options.set_headless(headless=True)
driver = webdriver.Chrome(chrome_options=options)
driver.get('http://data.discogs.com')
assert 'Discogs Data' in driver.title

pdb.set_trace()
