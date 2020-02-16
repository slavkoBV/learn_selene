import os

from selene.support.shared import browser
from selene.support.jquery_style_selectors import s, ss
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

    def search(self, query):
        s(".search-form__input[name=search]").set(query).press_enter()
        return SearchResult()


class UserPage:
    def sign_out(self):
        s("#profile_signout").click()


class SearchResult:
    def __init__(self):
        self.results = ss(".goods-tile__title")


def test_rozetka_sign_in_out():
    rozetka = RozetkaMainPage().load_page()
    sign_page = rozetka.login()
    sign_page.sign_in()
    s(".header-topline__user-link").should(have.no.text('увійдіть в особистий кабінет'))
    user_page = sign_page.load_user_page()
    user_page.sign_out()


def test_rozetka_search():
    rozetka = RozetkaMainPage().load_page()
    sign_page = rozetka.login()
    sign_page.sign_in()
    search_results = sign_page.search('moto g')
    for idx in range(5):
        search_results.results[idx].should(have.text("Moto G"))
    user_page = sign_page.load_user_page()
    user_page.sign_out()


if __name__ == '__main__':
    test_rozetka_sign_in_out()
    test_rozetka_search()
