# тестує лінки тільки на окремій сторінці, працює
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LinkTest:
    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        self.problem_links = set()

    def findAllLinks(self):
        wait = WebDriverWait(self.driver, 10)
        all_links = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
        links = set(all_links)

        for link in links:
            url = link.get_attribute("href")
            self.verify_link(url)

        self.driver.quit()
        self.write_problem_links_to_file()

    def verify_link(self, url):
        try:
            response = requests.head(url, timeout=10)

            if response.status_code == 200:
                print(f"{url} - {response.reason}")
            elif response.status_code in (404, 403, 500, 502, 503, 504):
                self.problem_links.add(f"{url} - Status code: {response.status_code} - Response - {response.reason} - is a broken link")
                print(f"{url} - Status code: {response.status_code} - Response - {response.reason} - is a broken link")
            elif response.status_code in (301, 302, 303, 307, 308):
                #передаю url до verify_link
                self.verify_link(response.headers.get('Location'))
            else:
                self.problem_links.add(f"{url} - Status code: {response.status_code} - Response - {response.reason}")
                print(f"{url} - Status code: {response.status_code} - Response - {response.reason}")

        except requests.RequestException as e:
            self.problem_links.add(f"{url} - Exception: {str(e)}")
            print(f"{url} - Exception: {str(e)}")

    def write_problem_links_to_file(self):
        with open("problem_links.txt", "w") as file:
            for link in self.problem_links:
                file.write(link + "\n")

linkTest = LinkTest('https://www.multiprojekt.pl')
linkTest.findAllLinks()
