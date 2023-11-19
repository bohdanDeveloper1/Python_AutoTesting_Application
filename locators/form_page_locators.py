# тут треба отримати всі поля які буду тетувати через id,  xpath
from selenium.webdriver.common.by import By
from random import randint

class Locators:
    # приклад як шукати елементи на сторінці
    FIRST_NAME = (By.CSS_SELECTOR,'#firstName')
    LAST_NAME = (By.CSS_SELECTOR,'#lastName')

