# знаходжу лінки заново після помилки
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, urljoin

class LinkTest:

    def __init__(self, url):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)
        self.base_url = url
        self.base_domain = urlparse(url).scheme + '://' + urlparse(url).hostname
        self.visited_links = set()
        self.problem_links = set()

    def findAllLinks(self, current_url=None):
        if current_url is None:
            current_url = self.base_url

        # Якщо current_url не починається із правильного домену
        if current_url in self.visited_links or not current_url.startswith(self.base_domain):
            return

        self.visited_links.add(current_url)

        try:
            self.driver.get(current_url)

            # чекаю поки всі лінки загрузяться на сторінці, максимальне очікування 10 секунд
            WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))

            # знаходжу всі лінки на поточній сторінці
            all_links = self.driver.find_elements(By.TAG_NAME, "a")

            # Перевірка кожного знайденого лінку
            # пошук всіх лінків на новій сторінці
            for link in all_links:
                try:
                    href = link.get_attribute("href")
                    full_url = urljoin(current_url, href)

                    if full_url.startswith(self.base_domain):
                        # Перевірка кожного знайденого лінку
                        self.verify_link(full_url)
                        # пошук всіх лінків на новій сторінці current_url
                        self.findAllLinks(current_url=full_url)

                # якщо знайденого лінку більше немає, знаходжу всі лінки на сторінці знову
                except StaleElementReferenceException:
                    print("StaleElementReferenceException: The element is no longer valid. Trying to find it again.")
                    # Повторне знаходження всіх лінків після виникнення помилки
                    all_links = self.driver.find_elements(By.TAG_NAME, "a")

        except Exception as e:
            print(f"An error occurred: {e}")

    def verify_link(self, url):
        try:
            response = requests.head(url, timeout=3)

            if response.status_code == 200:
                print(f"{url} - {response.reason}")

            else:
                print(f"{url} - Status code: {response.status_code} - Response - {response.reason}")
                self.problem_links.add(f"{url} - Status code: {response.status_code} - Response - {response.reason}")

        except requests.RequestException as e:
            print(f"An error occurred while verifying the link {url}: {e}")
            self.problem_links.add(f"{url} - Status code: N/A - Reason - Exception - is a broken link because of an undefined exception")

    def write_problem_links_to_file(self):
        with open("problem_links.txt", "w") as file:
            for link in self.problem_links:
                file.write(link + "\n")


# Приклад використання
linkTest = LinkTest('https://www.multiprojekt.pl')
linkTest.findAllLinks()
linkTest.write_problem_links_to_file()
