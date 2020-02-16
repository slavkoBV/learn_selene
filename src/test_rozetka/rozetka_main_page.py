import os

from selene.support.shared import browser
from selene.support.jquery_style_selectors import s
from selene.support.conditions import have


browser.config.browser_name = 'firefox'
browser.config.timeout = 5

email = os.environ.get("EMAIL")
password = os.environ.get("PASS")


class RozetkaMainPage:

    def load_page(self):
        browser.open('https://rozetka.com.ua/ua/')
        return self

    def login(self):
        s(".header-topline__user-link").click()
        return LoginPage()


class LoginPage:

    def sign_in(self):
        s("#auth_email").set(email).press_enter()
        s("#auth_pass").set(password).press_enter()
        return self

    def load_user_page(self):
        s("//a[contains(@href, 'personal-information')]").click()
        return UserPage()


class UserPage:

    def sign_out(self):
        s("#profile_signout").click()


def test_rozetka():
    rozetka = RozetkaMainPage().load_page()
    sign_page = rozetka.login()
    sign_page.sign_in()
    s(".header-topline__user-link").should(have.no.text('увійдіть в особистий кабінет'))
    user_page = sign_page.load_user_page()
    user_page.sign_out()


if __name__ == '__main__':
    test_rozetka()
