from testpage import OperationHelper
import logging
import time
import requests
import yaml
from send_to_email import send_mail

with open("testdata.yaml") as f:
    data = yaml.safe_load(f)
    name = data["username"]
    paswd = data["password"]
    test = data["test"]
    url_token = data["url_get_token"]
    url_api_posts = data["url_api_posts"]


def login_check(user, passwd, url, block):
    obj_data = requests.post(url=url,
                             data={'username': f'{user}',
                                   'password': f'{passwd}'})
    check_login = obj_data.json()[f'{block}']
    return str(check_login)


def token_auth(token, url, block):
    res = requests.get(url=url,
                       headers={"X-Auth-Token": token},
                       params={"owner": "Me"})
    content = [item[f"{block}"] for item in res.json()['data']]
    return content

def test_step1(browser):
    logging.info("Test1 Starting")
    testpage = OperationHelper(browser)
    testpage.go_to_site()
    testpage.enter_login("test")
    testpage.enter_pass("test")
    testpage.click_login_button()
    time.sleep(3)
    assert testpage.get_error_text() == "401", "Test_1 FAIL"


def test_step2(browser):
    logging.info("Test2 Starting")
    testpage = OperationHelper(browser)
    testpage.go_to_site()
    testpage.enter_login(name)
    testpage.enter_pass(paswd)
    testpage.click_login_button()
    time.sleep(2)
    assert testpage.get_profile_text() == f"Hello, {name}", "Test_2 FAIL"


def test_step3(browser):
    logging.info("Test3 Starting")
    testpage = OperationHelper(browser)
    testpage.click_to_do_new_post()
    testpage.enter_title("Hello, world")
    testpage.enter_description("help")
    testpage.enter_content("Bye, world")
    testpage.click_save_post_button()
    time.sleep(5)
    assert testpage.get_title_text() == "Hello, world", "Test_3 FAIL"


def test_step4(browser):
    logging.info("Test4 Starting")
    testpage = OperationHelper(browser)
    testpage.click_contact_button()
    testpage.enter_name("Mirov")
    testpage.enter_email("alex007@mail.ru")
    testpage.enter_contact_content("8652478495")
    testpage.contact_us_save_button()
    time.sleep(3)
    assert testpage.get_alert_text() == "Form successfully submitted", "Test_4 FAIL"