import time
import pinyin
from selenium import webdriver
import chromedriver_autoinstaller

Random_answer = 1


chromedriver_autoinstaller.install()

storylink = "https://www.zbschools.sg/stories-"
username = '*******@student.hci.edu.sg'
pw = ''
with open("zbbot.txt") as txt:
    startpost = int(txt.read())
increment = 1


def init_driver():
    # Create ChromeOptions if needed, otherwise, just return a new Chrome webdriver
    return webdriver.Chrome()



def remove(string, remove_str):
    return string.replace(remove_str, "")


def login(driver):
    driver.get("https://www.zbschools.sg/cos/o.x?c=/ca7_zbs/user&func=login")
    time.sleep(1)
    login_button = driver.find_element('xpath', "//a[@id='login']")
    login_button.click()
    user = driver.find_element('id', "inputLoginId")
    user.click()
    user.send_keys(username)
    password = driver.find_element('id', "inputPassword")
    password.click()
    password.send_keys(pw)
    submit_button = driver.find_element('id', "btn_submit")
    submit_button.click()


def do_quiz(driver):
    global startpost
    driver.get(storylink + str(startpost))
    current_url = str(driver.current_url)
    A1 = 1
    A2 = 0
    A3 = 0

    if current_url != storylink + str(startpost):
        startpost += 1
        with open("zbbot1.txt", "w") as txt:
            txt.write(str(startpost))
        return

    try:
        start_quiz_button = driver.find_element('xpath', "//a[@class='btn btn-assign']")
        start_quiz_button.click()
        time.sleep(1)
        passage = driver.find_element('xpath', "/html/body/div[1]/div/div/div/div/div[3]/div/div[1]/div[1]/div[6]").text
        passage = remove(passage, '"')
        driver.switch_to.frame('litebox_iframe')
        count = len(driver.find_elements('xpath', "/html/body/div/div/form/div[1]"))

        for q in range(1, count + 1):
            answer = ''
            try:
                question_text = driver.find_element('xpath', f"/html/body/div/div/form/div[{q}]/div[1]").text
            except:
                pass

            if '_' in question_text:
                try:
                    output = question_text.split('_')
                    a = passage.find(output[0])
                    b = passage.find(output[len(output) - 1])
                    r = range((b - a) - len(output[0]))
                    answer = ''.join(passage[n + a + len(output[0])] for n in r)
                except:
                    print('idk just crashed')
            else:
                try:
                    tpy = driver.find_element('xpath', f"/html/body/div/div/form/div[{q}]/div[1]/div[1]/h3/span/b/u").text
                    answer = pinyin.get(tpy)
                except:
                    print('stop crashing')

            options_count = len(driver.find_elements('xpath', f"//div[@class='quiz_question'][{q}]//td"))





            for a in range(1,5):
                A1 += 1
                option_text = driver.find_element('xpath', f"/html/body/div/div/form/div[{q}]/div[2]/table/tbody/tr[{a}]/td[2]").text
                option_text = remove(option_text, " ")
                option = driver.find_element('xpath', f"//html/body/div/div/form/div[{q}]/div[2]/table/tbody/tr[{a}]/td[1]")

                if answer == option_text:
                    option.click()

        submit_button = driver.find_element('xpath', "/html/body/div/div/form/div[5]/input")
        submit_button.click()

    except Exception as e:
        print(f"An error occurred: {e}")

    startpost += 1


while True:
    try:
        driver = init_driver()
        login(driver)

        while True:
            if login(driver):
                # Successfully logged in, proceed with the quiz
                do_quiz(driver)
                startpost += 1
                print(startpost)
                with open("zbbot.txt", "w") as txt:
                    txt.write(str(startpost))
            else:
                # Unable to login, perform actions related to failure (e.g., try again, print an error message, etc.)
                print("Login failed, attempting quiz anyway")
                do_quiz(driver)
                startpost += 1
                print(startpost)
                with open("zbbot.txt", "w") as txt:
                    txt.write(str(startpost))

    except Exception as e:
        print(f"An error occurred: {e}")
