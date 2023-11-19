from pages.base_page import BasePage
from locators.form_page_locators import Locators

class FormPage(BasePage):

    def fill_fields_and_submit(self):
        #заповнюю поля данними
        #return дані які заповнив у поля, щоб перевірити чи форма отримала ті самі дані
        first_name = 'First name'
        last_name  = 'Last name'
        email      = 'email@example.com'
        self.element_is_visible(Locators.FIRST_NAME).send_keys(first_name)
        self.element_is_visible(Locators.LAST_NAME).send_keys(last_name)
        return first_name, last_name, email


    def form_result(self):
        result_list = self.element_are_visible(Locators.elements_on_page)
        result_text = []
        for i in result_list:
            result_text.append(i.text)

        return result_text
