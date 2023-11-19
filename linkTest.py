import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

class LinkTest:

    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.driver.get(url)

    def findAllLinks(self):
        # Znajdowanie wszystkich dostępnych linków na stronie
        self.driver.implicitly_wait(2)
        # додати перевіку ще для кнопок
        links = self.driver.find_elements(By.TAG_NAME, "a")

        # Get the number of links
        num_links = len(links)

        # Iteracja po linkam
        for i in range(num_links):
            link = links[i]
            url = link.get_attribute("href")
            self.verify_link(url)

        self.driver.quit()

    def verify_link(self, url):
        try:
            response = requests.head(url, timeout=3)

            if response.status_code == 200:
                print(f"{url} - {response.reason}")
            elif response.status_code in (301, 302, 307, 308):
                # Wykonujemy nowe żądanie GET do nowego adresu URL i sprawdzamy jego status
                new_url = response.headers.get('Location')
                new_response = requests.head(new_url, timeout=6)

                if new_response.status_code == 200:
                    print(f"{url} - {response.reason}")
                else:
                    print(f"{url} - {response.reason} - redirects to a broken link ({new_url})")
            else:
                print(f"{url} - {response.reason} - is a broken link")
        except requests.RequestException:
            print(f"{url} - is a broken link")


#linkTest = LinkTest('https://www.multiprojekt.pl')
linkTest = LinkTest('https://www.multiprojekt.pl/katalog/pl/zapytanie-ofertowe')
linkTest.findAllLinks()


