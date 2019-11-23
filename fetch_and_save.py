from datetime import datetime as dt
import datetime
import requests
import zipfile
import io
import os


def fetch_link():
    """
    Fetches the link for the latest Bhavcopy from BSE website.
    It uses a headless chrome instance t
    """
    from selenium import webdriver

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(
        executable_path='./chromedriver', options=chrome_options)

    LINK_XPATH = '//*[(@id = "ContentPlaceHolder1_btnhylZip")]'

    driver.get("https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx")
    link = driver.find_element_by_xpath(LINK_XPATH).get_attribute("href")
    driver.close()
    return link


def save_zip() -> None:
    """
    Fetches the bhavcopy and extracts the csv file.
    """
    request_url = fetch_link()
    r = requests.get(request_url)
    if r.ok:
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall()
        os.rename(request_url.split("/")
                  [-1].strip(".ZIP").replace("_", "."), "temp.csv")
    else:
        print("Request failed")


def convert_helper(data):
    """
    Redis converts all data within a dict in bytes.
    This function converts data back to string.
    """
    if isinstance(data, bytes):
        return data.decode('ascii')
    if isinstance(data, dict):
        return dict(map(convert_helper, data.items()))
    if isinstance(data, tuple):
        return map(convert_helper, data)
    return data
