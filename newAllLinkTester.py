import requests
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, urljoin

class LinkTest:
    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        # Tworzenie pustego słownika do przechowywania informacji o URL-ach
        self.url_list = [{url: {'status_code': 0, 'checked': False}}]
        self.base_url = url
        # виділяє домен з url
        self.base_domain = urlparse(url).scheme + '://' + urlparse(url).hostname
        self.checked_links = set()
        self.problem_links = set()

        # Відкриття файлу для запису помилок
        self.error_file_path = "problem_links.txt"
        self.error_file = open(self.error_file_path, "w")

    # __del__ викликається коли видаляються всі посилання на об'єкт
    # або коли програма завершується
    def __del__(self):
        # Закриття файлу при завершенні роботи програми
        if self.error_file:
            self.error_file.close()

    def log_error(self, error_message):
        # Запис помилок у файл
        self.error_file.write(error_message + "\n")
        self.error_file.flush()  # Забезпечення виводу в файл без затримки

    # поки в url_info є 'checked': False, функція передає НЕПЕРЕВІРЕНІ url до checkLinkStatus
    def ifNotAllLinksChecked(self):
        for url_info in self.url_list:
            for url, info in url_info.items():
                if not info['checked']:
                    self.checkLinkStatus(url)


    # дописати логіку для лінків із перенаправленнями
    def checkLinkStatus(self, url):
        # якщо лінк вже був перевірений то return
        # не перевіряти лінки із перенаправленнями
        if url in self.checked_links or url in self.problem_links:
            return

        try:
            # отримую статус код лінку
            response = requests.head(url, timeout=10)

            # записую лінк як перевірений
            self.url_list.append({url: {'status_code': response.status_code, 'checked': True}})
            self.checked_links.add(url)

            # перевіряю статус код лінку, якщо = 200 то буду шукати лінки на новій сторінці findAllLinksByCurrentUrl
            if response.status_code == 200:
                print(f"{url} - {response.reason}")
                self.findAllLinksByCurrentUrl(url)

            # якшо перенаправлення то передаю url до checkLinkStatus та перевіряю ще раз
            elif response.status_code in (301, 302, 303, 307, 308):
                self.checkLinkStatus(response.headers.get('Location'))

            #  якщо татус код лінку != 200, записую лінк як проблемний
            else:
                # записую проблемний лінк до словника як перевірений із status_code': 0, щоб він більше не перевірявся
                self.url_list.append({url: {'status_code': 0, 'checked': True}})
                error_message = f"{url} - Status code: {response.status_code} - Response - {response.reason}"
                print(error_message)
                self.problem_links.add(url)
                self.log_error(error_message)

        except requests.RequestException as e:
            # записую проблемний лінк до словника як перевірений із status_code': 0, щоб він більше не перевірявся
            self.url_list.append({url: {'status_code': 0, 'checked': True}})
            error_message = f"exception with {url}: {e}"
            print(error_message)
            self.problem_links.add(url)
            self.log_error(error_message)

    # шукаю всі лінки на новій сторінці і додаю їх до словника
    def findAllLinksByCurrentUrl(self, url):
        if not url.startswith(self.base_domain):
            return

        try:
            # перехожу на нову сторінку
            self.driver.get(url)

            # чекаю поки всі лінки загрузяться на сторінці, максимальне очікування 10 секунд
            WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))

            # знаходжу всі лінки на поточній сторінці
            all_links = self.driver.find_elements(By.TAG_NAME, "a")

            # записую все що знайшов до url_list
            for link in all_links:
                self.url_list.append({link.get_attribute("href"): {'status_code': 0, 'checked': False}})

        except Exception as e:
            # todo якщо помилка буде повторюватимь у файлі txt, то иожливо треба додати
            #  self.url_list.append({url: {'status_code': 0, 'checked': True}})
            error_message = f"{url} - exception {e}"
            print(error_message)
            self.problem_links.add(url)
            self.log_error(error_message)

        def write_problem_links_to_file(self):
            # Закриття файлу перед виходом з програми
            if self.error_file:
                self.error_file.close()

linkTest = LinkTest('https://www.multiprojekt.pl')
linkTest.ifNotAllLinksChecked()
linkTest.write_problem_links_to_file()