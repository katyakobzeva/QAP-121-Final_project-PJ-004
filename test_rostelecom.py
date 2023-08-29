from time import sleep
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from main import AuthForm, CodeForm
from settings import valid_email, valid_password, valid_number

# фикстура для запуска тестов
@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Firefox('')
    driver.implicitly_wait(3)
    driver.maximize_window()

    yield driver

    driver.quit()

# ТК-001 (Присутствуют поля для ввода данных клиента для аутентификации)
def test_phone_by_default(selenium):
    form = AuthForm(selenium)

    assert form.placeholder.text == 'Мобильный телефон'


# TК-003 (Авторизация клиента по номеру телефона, кнопка "Номер")
def test_auth_reg_phone(selenium):
    form = AuthForm(selenium)

    # Вводим номер телефона и пароль
    form.username.send_keys(valid_number)
    form.password.send_keys(valid_password)
    sleep(20) # если появления Captcha, вводится вручную
    form.btn_click()

    assert form.get_current_url() == '/account_b2c/page'


# TК-004 (Авторизация клиента по номеру телефона, кнопка "Номер" с некорректным паролем)
def test_auth_fake_phone(selenium):
    form = AuthForm(selenium)

    # Вводим номер телефона и пароль
    form.username.send_keys('+79177733624')
    form.password.send_keys('1234к56')
    sleep(20) # если появления Captcha, вводится вручную
    form.btn_click()

    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'


# TК-005 (Авторизация клиента по эл.почте, кнопка "Почта")
def test_auth_reg_email(selenium):
    form = AuthForm(selenium)

    # Вводим e-mail и пароль
    form.username.send_keys(valid_email) #нужно дописать test перед 03 в поле ввода почты
    form.password.send_keys(valid_password)
    sleep(20) # если появится Captcha, вводится вручную
    form.btn_click()

    assert form.get_current_url() == '/account_b2c/page'


# TК-010 (Авторизация клиента по эл.почте с некорректными данными, кнопка "Почта")
def test_auth_fake_email(selenium):
    form = AuthForm(selenium)

    # Вводим e-mail и пароль
    form.username.send_keys('error404@mail.com')
    form.password.send_keys('jfbyfng')
    sleep(20) # если появится Captcha, вводится вручную
    form.btn_click()

    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'

# TК-008 (Авторизация клиента по временному коду)
def test_auth_code(selenium):
    form = CodeForm(selenium)

    # Вводим номер телефона
    form.address.send_keys(valid_number)

    sleep(30) # если появится Captcha, вводится вручную
    form.get_click()

    otc = form.driver.find_element(By.ID, 'rt-code-0')
    assert otc

# TК-009 (Отображение формы "Восстановление пароля" на странице)
def test_recovery(selenium):
    form = AuthForm(selenium)

    # Нажатие на кнопку "Забыл пароль"
    form.forgot.click()
    sleep(5)

    reset_pass = form.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/h1')

    assert reset_pass.text == 'Восстановление пароля'

# TК-010 (Отображение формы "Регистрация" на странице)
def test_reg_form(selenium):
    form = AuthForm(selenium)

    # Нажатие на кнопку "Зарегистрироваться"
    form.register.click()
    sleep(5)

    reset_pass = form.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/h1')

    assert reset_pass.text == 'Регистрация'


# TК-011 (Авторизация через соц.сеть "ВКонтакте")
def test_auth_vk(selenium):
    form = AuthForm(selenium)
    form.vk_btn.click()
    sleep(5)

    assert form.get_base_url() == 'id.vk.com'


# TК-012 (Авторизация через соц.сеть "Одноклассники")
def test_auth_ok(selenium):
    form = AuthForm(selenium)
    form.ok_btn.click()
    sleep(5)

    assert form.get_base_url() == 'connect.ok.ru'

# TК-013 (Авторизация через соц.сеть "Мой Мир")
def test_auth_mail_ru(selenium):
    form = AuthForm(selenium)
    form.mail_ru_btn.click()
    sleep(5)

    assert form.get_base_url() == 'connect.mail.ru'


# ТК-014 (Авторизация через "Яндекс.Паспорт")
def test_auth_yandex(selenium):
    form = AuthForm(selenium)
    form.yandex_btn.click()
    sleep(5)

    assert form.get_base_url() == 'passport.yandex.ru'


 #TК-018 (В подвале страницы есть ссылка с Пользовательским соглашением)
def test_user_agreement(selenium):
    form = AuthForm(selenium)

    original_window = form.driver.current_window_handle
    # Нажатие на кнопку "Пользовательским соглашением" в подвале страницы
    form.agree.click()
    sleep(5)
    WebDriverWait(form.driver, 5).until(EC.number_of_windows_to_be(2))
    for window_handle in form.driver.window_handles:
        if window_handle != original_window:
            form.driver.switch_to.window(window_handle)
            break
    title_page = form.driver.execute_script("return window.document.title")

    assert title_page == 'User agreement'




