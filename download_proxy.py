import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    return driver


def save_proxies_to_files(content: str):
    with open("proxies.txt", "w") as f:
        f.write(content)


def get_proxies():
    driver = get_driver()
    driver.get('https://spys.one/en/')
    _ = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "spy14")))
    pattern = re.compile(r'\d{1,4}.\d{1,4}.\d{1,4}.\d{1,4}:\d{1,6}')
    text = ','.join([x.text for x in driver.find_elements(by=By.CLASS_NAME, value='spy14')])
    matches = '\n'.join(pattern.findall(text))
    save_proxies_to_files(matches)
    driver.close()


if __name__ == '__main__':
    get_proxies()
