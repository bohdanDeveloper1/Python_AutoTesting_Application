from urllib.parse import urlparse, urljoin
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class LinkTest:
    def __init__(self, url, txt_name):
        # uruchamiam driver
        self.driver = webdriver.Chrome()
        # wchodzę do strony
        self.driver.get(url)
        # tworzę słownik z danymi
        self.website_data = {
            f"{url}": {
                "source_url": f"{url}",
                "status": "",
                "checked": False
            }
        }
        self.base_url = url
        # domen strony
        self.base_domain = urlparse(url).scheme + '://' + urlparse(url).hostname
        # tworze plik dla zapisywania błędów
        self.error_file_path = txt_name
        self.error_file = open(self.error_file_path, "w", encoding="utf-8")

    def ifNotAllLinksChecked(self):
        # dopóki w slowniku self.website_data jest "checked": False
        while any(not entry["checked"] for entry in self.website_data.values()):
            # tworze kopię słownika do iteracji
            # bez kopii słownika, zgłaszany jest błąd, że obiekt zmienia rozmiar podczas iteracji
            website_data_copy = self.website_data.copy()
            for url, data in website_data_copy.items():
                # szukam 'checked' == False
                if not data["checked"]:
                    # sprawdzam link
                    self.checkLinkStatus(url)

    # zamknięcie pliku i driver-a po zakończeniu programu
    def __del__(self):
        if self.error_file:
            self.error_file.close()

        self.driver.quit()

    # Zapisywanie błędów do pliku txt
    def log_error(self, error_message):
        self.error_file.write(error_message + "\n")
        self.error_file.flush()

    def checkLinkStatus(self, url):
        if url.endswith(".docx"):
            self.website_data[url]["checked"] =  True
            return

        # dla wyjątków, kiedy url-a niema w self.website_data.keys()
        if url not in self.website_data.keys():
            self.website_data[url] = {
                "source_url": url,
                "checked": True
            }

        try:
            # otrzymuje status kod URL-a
            response = requests.head(url, timeout=10)

            if response.status_code == 200:
                # zmieniam checked na True
                self.website_data[url]["checked"] = True
                self.website_data[url]["status"] = response.status_code
                print(f"{url} - {response.reason}")
                # szukam linków na danej stronie
                self.findAllLinksByCurrentUrl(url)

            # jeśli jest przekierowanie, to przekazuję adres URL do checkLinkStatus i sprawdzam go ponownie
            elif response.status_code in (301, 302, 303, 307, 308):
                self.website_data[url]["checked"] = True
                self.website_data[url]["status"] = response.status_code
                self.checkLinkStatus(response.headers.get('Location'))

            else:
                # zmieniam checked na True
                self.website_data[url]["checked"] = True
                self.website_data[url]["status"] = response.status_code
                # zapisuje problem do pliku txt oraz konsoli
                problem = f"{url} - status - {response.status_code}, problem during checkLinkStatus, parent is {self.website_data[url]["source_url"]}"
                self.log_error(problem)
                print(problem)

        except requests.RequestException as e:
            self.website_data[url]["checked"] = True
            self.website_data[url]["source_url"] = self.website_data[url]["source_url"]
            problem = f"{url} exception: {e}, parent is {self.website_data[url]["source_url"]}"
            self.log_error(problem)
            print(problem)

    # przekazuje tylko linki ze status code = 200
    def findAllLinksByCurrentUrl(self, full_url):
        # dla linków którę mają inny domen
        if not full_url.startswith(self.base_domain):
            return

        # nie szukam linków dla .pdf, .jpg, .docx
        if full_url.endswith(".pdf") or full_url.endswith(".jpg") or full_url.endswith(".docx"):
            return

        try:
            # wchodzę na nową stronę
            self.driver.get(full_url)

            # czekam, aż wszystkie linki załadują się na stronie, maksymalny czas oczekiwania 10 sekund
            WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))

            # znajdauje wszystkie linki na bieżącej stronie
            all_links = self.driver.find_elements(By.TAG_NAME, "a")

            # Zapisuję href i source_url do słownika
            for link in all_links:
                href = link.get_attribute("href")
                correct_url = urljoin(self.base_url, href)
                # Dodajemy nowy wpis do słownika, jeżeli takiego wpisu jeszcze niema
                if correct_url not in self.website_data.keys():
                    self.website_data[correct_url] = {
                        "source_url": full_url,
                        "checked": False
                    }

        except Exception as e:
            self.website_data[full_url] = {
                "source_url": full_url,
                "checked": True
            }
            problem = f"exception during finding urls in {full_url}: {e}, parent is {full_url}"
            self.log_error(problem)
            print(problem)

    def write_problem_links_to_file(self):
        # zamknięcie pliku przed wyjściem z programu
        if self.error_file:
            self.error_file.close()


linkTest = LinkTest('https://www.multiprojekt.pl', "problem_links.txt")
linkTest.ifNotAllLinksChecked()
linkTest.write_problem_links_to_file()
