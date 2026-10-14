import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import quote, unquote


@pytest.fixture
def browser():
    driver = webdriver.Chrome()

    yield driver

    driver.quit()


def test_successful_booking(
    browser,
    clubs,
    competitions,
):

    club = clubs[0]
    competition = competitions[0]
    places_required = 5

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

    assert browser.current_url == 'http://127.0.0.1:5000/show-summary'
    assert club['email'] in browser.page_source
    assert competition['name'] in browser.find_element(
        By.TAG_NAME,
        'body'
    ).text

    booking_link = browser.find_element(
        By.CSS_SELECTOR,
        f'a[href="/book/{quote(competition['name'])}/{quote(club['name'])}"]'
    )

    booking_link.click()

    assert (
        unquote(browser.current_url)
        == f"http://127.0.0.1:5000/book/{competition['name']}/{club['name']}"
    )
    assert club['name'] in browser.page_source
    assert competition['name'] in browser.page_source

    places_required_input = browser.find_element(By.NAME, 'places')
    places_required_input.send_keys(places_required)

    purchase_button = (
        browser.find_element(
            By.CSS_SELECTOR,
            'button[type="submit"]'
        )
    )
    purchase_button.click()

    expected_club_points_after_booking = (
        int(club['points'])
        - places_required
    )

    expected_competition_places_after_booking = (
        int(competition['number_of_places'])
        - places_required
    )

    page_text = browser.find_element(By.TAG_NAME, 'body').text

    assert browser.current_url == 'http://127.0.0.1:5000/purchase-places'
    assert club['email'] in page_text
    assert (
        f'Points available: {expected_club_points_after_booking}'
        in page_text
    )
    assert (
        f'Number of Places: {expected_competition_places_after_booking}'
    ) in browser.find_element(
        By.XPATH,
        f'//li[contains(., "{competition["name"]}")]'
    ).text
    assert 'Success-Booking complete!' in page_text
