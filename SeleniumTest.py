from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from random import randint

class FormTest:

    def __init__(self, url):
        # Inicjujemy przeglądarkę jako atrybut klasy
        self.driver = webdriver.Chrome()
        self.driver.get(url)

    def dataInputIntoForm(self):
        #dane, które wprowadzę w pola formularza
        self.first_name_value, self.last_name_value, self.email_value = 'Bob', 'Test', 'email@gmail.com'
        self.mobile_value = '3232322322'

        # Usulam stopkę z DOM, aby nie przeszkodzala klikac w przycisk
        self.driver.execute_script("document.getElementsByTagName('footer')[0].remove();")
        self.driver.execute_script('document.getElementById("fixedban").style.display="none";')
        # ustawiam oczekiwania dla przeglądarki w zakresie wyszukiwania elementów
        self.driver.implicitly_wait(0.5)

        self.findElementsOfFormAndInputData()

    def findElementsOfFormAndInputData(self):
        # Znajduję element i wypełniam go danymi
        self.first_name = self.driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/div[2]/div[2]/form/div[1]/div[2]/input').send_keys(self.first_name_value)
        self.last_name = self.driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/div[2]/div[2]/form/div[1]/div[4]/input').send_keys( self.last_name_value)
        self.email = self.driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/div[2]/div[2]/form/div[2]/div[2]/input').send_keys( self.email_value)

        #{randint(1,3)}
        self.gender = self.driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/div[2]/div[2]/form/div[3]/div[2]/div[2]/label').click()
        self.mobile = self.driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/div[2]/div[2]/form/div[4]/div[2]/input').send_keys( self.mobile_value)
        self.submit_button = self.driver.find_element(By.CSS_SELECTOR,'#submit').click()
        self.driver.implicitly_wait(0.5)

        self.getResultAfterSendingForm()

    def getResultAfterSendingForm(self):
        # Otrzymuję wynik z formularza
        self.name_text =  self.driver.find_element(By.XPATH,'/html/body/div[5]/div/div/div[2]/div/table/tbody/tr[1]/td[2]').text
        self.email_text =  self.driver.find_element(By.XPATH,'/html/body/div[5]/div/div/div[2]/div/table/tbody/tr[2]/td[2]').text
        self.mobile_text =  self.driver.find_element(By.XPATH,'/html/body/div[5]/div/div/div[2]/div/table/tbody/tr[4]/td[2]').text
        self.driver.implicitly_wait(0.5)

        self.checkIfInutDataEqualResultData()

    def checkIfInutDataEqualResultData(self):
        # Sprawdzam czy wprowadzone dane == wynik
        print('first_name and last_name test passed' if  f'{self.first_name_value} {self.last_name_value}' == self.name_text else 'Form not filled correctly. Problem with first_name or last_name.')
        print('email test passed' if self.email_value == self.email_text else 'Form not filled correctly. Problem with email.')
        print('mobile number test passed' if self.mobile_value == self.mobile_text else 'Form not filled correctly. Problem with mobile.')

        self.driver.quit()


formTest = FormTest('https://demoqa.com/automation-practice-form')
formTest.dataInputIntoForm()

# Wait(5).until(EC.visibility_of_element_located(By.CSS_SELECTOR,'#firstName')).send_keys(first_name)
# Wait(5).until(EC.visibility_of_element_located(By.CSS_SELECTOR,'#lastName')).send_keys(last_name)

# assert f'{first_name} {last_name}' == result[0], 'Form not filled correctly. Problem with first_name or last_name.'
# assert email == result[1], 'Form not filled correctly. Problem with email.'