import requests
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, urljoin

# todo may should add StaleElementReferenceException
class LinkTest:
    def __init__(self, url):
        # запускаю драйвер та перехожу по посиланню
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        # Tworzenie słownika do przechowywania informacji o URL-ach
        # todo url_list зробити простіше, щоб я розумів, працювати на простих об'єктах
        # програма зациклюється, бо я не змінюю 'checked': False на True
        self.url_list = [url]
        # домен сайту
        self.base_url = url
        # виділяє домен з url
        self.base_domain = urlparse(url).scheme + '://' + urlparse(url).hostname
        self.checked_links = set()
        self.problem_links = set()

        # Відкриття файлу для запису помилок
        self.error_file_path = "newaAllLinkTester_problem_links.txt"
        self.error_file = open(self.error_file_path, "w", encoding="utf-8")

    # __del__ викликається коли видаляються всі посилання на об'єкт
    # або коли програма завершується
    # Закриття файлу та драйверу після завершенні роботи програми
    def __del__(self):
        if self.error_file:
            self.error_file.close()

        self.driver.quit()

    def log_error(self, error_message):
        # Запис помилок у файл
        self.error_file.write(error_message + "\n")
        self.error_file.flush()  # Забезпечення виводу в файл без затримки

    # поки в url_info є 'checked': False, функція передає НЕПЕРЕВІРЕНІ url до checkLinkStatus
    def ifNotAllLinksChecked(self):
        for url in self.url_list:
            self.checkLinkStatus(url)

    # todo переробити всі додавання values до lиста
    # todo File "C:\Users\Acer\PycharmProjects\pythonProject\newAllLinkTester.py", line 102, in findAllLinksByCurrentUrl
    # AttributeError: 'NoneType' object has no attribute 'startswith'
    def checkLinkStatus(self, url):
        # якщо лінк вже був перевірений то return
        # не перевіряти лінки із перенаправленнями
        if url in self.checked_links or url in self.problem_links:
            return

        # знаходжу правильний url за допомогою urljoin
        full_url = urljoin(self.base_url, url)

        try:
            # Otrzymujesz status kod pełnego URL
            response = requests.head(full_url, timeout=10)

            # записую лінк як перевірений
            self.checked_links.add(full_url)

            # перевіряю статус код лінку, якщо = 200 то буду шукати лінки на новій сторінці findAllLinksByCurrentUrl
            if response.status_code == 200:
                print(f"{full_url} - {response.reason}")
                self.findAllLinksByCurrentUrl(full_url)

            # якшо перенаправлення то передаю url до checkLinkStatus та перевіряю ще раз
            elif response.status_code in (301, 302, 303, 307, 308):
                self.checkLinkStatus(response.headers.get('Location'))

            #  якщо татус код лінку != 200, записую лінк як проблемний
            else:
                error_message = f"{full_url} - Status code: {response.status_code} - Response - {response.reason}"
                print(error_message)
                self.problem_links.add(full_url)
                self.log_error(error_message)


        except requests.RequestException as e:
            self.checked_links.add(full_url)
            error_message = f"exception with {full_url}: {e}"
            print(error_message)
            self.problem_links.add(full_url)
            self.log_error(error_message)

    # шукаю всі лінки на новій сторінці і додаю їх до словника
    def findAllLinksByCurrentUrl(self, full_url):
        # todo тут проблема з startswith, не оперує на об'єктах
        if not full_url.startswith(self.base_domain):
            return

        try:
            # перехожу на нову сторінку
            self.driver.get(full_url)

            # чекаю поки всі лінки загрузяться на сторінці, максимальне очікування 10 секунд
            WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))

            # знаходжу всі лінки на поточній сторінці
            all_links = self.driver.find_elements(By.TAG_NAME, "a")

            # записую все що знайшов до url_list
            for link in all_links:
                href = link.get_attribute("href")
                founded_url_from_parent_link = urljoin(self.base_url, href)
                if founded_url_from_parent_link not in self.checked_links and link not in self.problem_links:
                    # todo перевіряти лінк, якщо статус != 200
                    response = requests.head(founded_url_from_parent_link, timeout=3)
                    if response.status_code not in (200, 301, 302, 303, 307, 308):
                        problem = f"{founded_url_from_parent_link} - {response.reason}, parent url is: {full_url} "
                        print(problem)
                        self.log_error(problem)
                        self.problem_links.add(problem)
                        self.checked_links.add(problem)
                    else:
                        self.url_list.append(founded_url_from_parent_link)

        except Exception as e:
            error_message = f"{full_url} - exception {e}"
            print(error_message)
            self.problem_links.add(full_url)
            self.checked_links.add(full_url)
            self.log_error(error_message)


    def write_problem_links_to_file(self):
        # Закриття файлу перед виходом з програми
        if self.error_file:
            self.error_file.close()

linkTest = LinkTest('https://www.multiprojekt.pl')
linkTest.ifNotAllLinksChecked()
linkTest.write_problem_links_to_file()