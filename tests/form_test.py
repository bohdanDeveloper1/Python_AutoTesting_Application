from pages.form_page import FormPage

class TestFormPage:

    def test_form(self, driver):
        form_page = FormPage(driver, 'https://demoqa.com/automation-practice-form')
        form_page.open()
        #функція повертає дані які я вказав
        first_name, last_name, email =  form_page.fill_fields_and_submit()
        result = form_page.form_result()
        assert f'{first_name} {last_name}' == result[0], 'Form not filled correctly. Problem with first_name or last_name.'
        assert email == result[1], 'Form not filled correctly. Problem with email.'


