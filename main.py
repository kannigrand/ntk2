from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from sys import platform


def get_browser(hiden_key):
    options = webdriver.ChromeOptions()
    if hiden_key:
        options.add_argument('headless')

    if platform == "linux" or platform == "linux2":
        browser = webdriver.Chrome(executable_path="chromedriver", options=options)
        return browser
    elif platform == "win32":
        browser = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
        return browser
    else:
        print("OS not supported")
        return False


def parser(ident, hiden_key=True):
    """
    ident строковый идентификатор по которому получать данные компании (инн, огрн онргип)
    если нужно чтобы окно браузера отображалось передай вторым именнованным аргуметом False
    """
    browser = get_browser(hiden_key)
    if not browser:
        return ()

    try:
        browser.get("https://egrul.nalog.ru/index.html")
        wait = WebDriverWait(browser, 10)
        inp = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="query"]')))
        inp.clear()
        inp.send_keys(ident)
        browser.find_element_by_xpath('//*[@id="btnSearch"]').click()
        res_mane = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="resultContent"]/div/div[2]/a'))).text
        res_data = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="resultContent"]/div/div[3]/div'))).text
        return res_mane, res_data
    except TimeoutException:
        return ()


if __name__ == '__main__':
    idn = "7714964363"
    print(parser(idn))
    idn = "636300079791"
    print(parser(idn))