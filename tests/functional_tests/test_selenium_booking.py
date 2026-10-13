import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import unquote


@pytest.fixture
def browser():
    driver = webdriver.Chrome()

    yield driver

    driver.quit()


def test_successfull_booking(
    browser,
    clubs,
    competitions
):

    club = clubs[0]
    competition = competitions[0]

    browser.get('http://127.0.0.1:5000/')
    email_input = browser.find_element(By.NAME, 'email')
    email_input.send_keys(club['email'])

    assert browser.current_url == 'http://127.0.0.1:5000/'
    assert email_input.get_attribute('value') == club['email']

    summary_button = browser.find_element(
        By.CSS_SELECTOR,
        'button[type="submit"]'
    )
    summary_button.click()

    assert browser.current_url == 'http://127.0.0.1:5000/showSummary'
    assert club['email'] in browser.page_source
    assert competition['name'] in browser.find_element(
        By.TAG_NAME,
        'body'
    ).text

    booking_link = browser.find_element(
        By.CSS_SELECTOR,
        f'a[href="/book/{competition['name']}/{club['name']}"]'
    )

    booking_link.click()

    assert (
        unquote(browser.current_url)
        == f"http://127.0.0.1:5000/book/{competition['name']}/{club['name']}"
    )