import re
import time
import pinyin
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By

Random_answer = 1
storylink = "https://www.zbschools.sg/stories-"
username = ''
pw = ''

chromedriver_autoinstaller.install()

driver = webdriver.Chrome()
regex = ""

with open("zbbot.txt") as txt:
    startpost = int(txt.read())
increment = 1

def WaitTill(element, tag=None, content=None):
    if (tag == None):
        while True:
            try:
                return driver.find_element('xpath', element)
            except:
                pass
    else:
        while True:
            try:
                return driver.find_element('xpath', "//" + element + "[@" + tag + "='" + content + "']")
            except:
                pass

#//*[@id="quizform"]/div[1]/div[1]/div[1]/h3/span/text()[1]

def init_driver():
    # Create ChromeOptions if needed, otherwise, just return a new Chrome webdriver
    return webdriver.Chrome()



def remove(string, remove_str):
    return string.replace(remove_str, "")

username = '221496R@student.hci.edu.sg'
pw = 'HCIPassword6969'

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
    global startpost
    driver.get(storylink + str(startpost))
    currentUrl = str(driver.current_url)
    if (currentUrl != storylink + str(startpost)):
        startpost += 1
        with open("zbbot.txt", "w") as txt:
            txt.write(str(startpost))
        return

def Quiz_py():
    startquiz = driver.find_element('xpath','//*[@id="lo_main"]/div/div[3]/div/div[1]/div[1]/div[3]/div/div/a[4]')
    startquiz.click()
    time.sleep(1)
    driver.switch_to.frame('litebox_iframe')
    qcount = len(driver.find_elements('xpath', "/html/body/div/div/form/div"))
    for q in range(1,qcount+1):
        answer = ""
        try:
            text = driver.find_element(By.ID, 'quizform').text
        except:
            regex.append(q)

        try:
            tpy = driver.find_element('xpath', f"/html/body/div/div/form/div[{q}]/div[1]/div[1]/h3/span/b").text
            answer = pinyin.get(tpy)
        except:
            ('stop crashing')
        qcount = len(driver.find_elements('xpath', f"/html/body/div/div/form/div[{q}]/div[2]/table/tbody/tr"))
        for a in range(1, qcount + 1):
            optext = driver.find_element('xpath',
                                         f"/html/body/div/div/form/div[{q}]/div[2]/table/tbody/tr[{a}]/td[2]").text
            optext = (remove(optext, " "))
            opt = driver.find_element('xpath',
                                      f"/html/body/div/div/form/div[{q}]/div[2]/table/tbody/tr[{a}]/td[1]/input")
            if answer == optext:
                opt.click()
    submit = driver.find_element('xpath', f"/html/body/div/div/form/div[{count}]/input")
    submit.click()
def Quiz_re():
    result_string = ''
    for element in driver.find_elements('xpath', '//*[@class="term"]'):
        result_string += element.text
# result_string is the entire passage of the article
    passage = result_string
    pattern = driver.find_element('xpath','//*[@id="quizform"]/div[regex]/div[1]/div[1]/h3/span')

    # Search for the pattern in the passage o
    match = re.search(pattern, passage)

    # Check if a match is found
    if match:
        # Extract the content within the parentheses (capturing group)
        answer = match.group(1)
        answer_choices = ""
        acount = len('xpath','//*[@id="quizform"]/div[3]/div[2]/table')
        for i in range(1, acount+1):
            answer_choices.append('xpath',f'//*[@id="quizform"]/div[3]/div[2]/table/tbody/tr[{i}]/td[2]')
        # Gave the answer choices in the list
        # Check which answer choice matches the extracted answer using regex
        matching_choice = None
        for choice in answer_choices:
            choice_pattern = re.escape(choice.split('.')[1].strip())
            if re.search(choice_pattern, answer):
                matching_choice = choice
                break
        # Print the result
        if matching_choice:
            y = answer_choices.index(choice) + 1
            Answer_btn = ('xpath', f'f"/html/body/div/div/form/div[{y}]/input"')
            Answer_btn.click()
        else:
            print("No matching answer choice found.")
    else:
        print("Pattern not found in the passage.")
        #try and make it to repeating quizzes or make numbers available



def do_quiz(driver):
        Quiz_py()
        Quiz_re()

while(True):
    login(driver)
    do_quiz(driver)

























































"""
    try:
        startquiz = driver.find_element('xpath', "//a[@class='btn btn-assign']")
        startquiz.click()
        time.sleep(1)
        passage = driver.find_element('xpath', "html/body/div/div/div/div/div/div[3]/div/div[1]/div[1]/div[6]").text
        passage = remove(passage, '"')
        driver.switch_to.frame('litebox_iframe')
        count = len(driver.find_elements('xpath', "/html/body/div/div/form/div"))
        for q in range(1, count):
            answer = ''
            try:
                text = driver.find_element('xpath', f"/html/body/div/div/form/div[{q}]/div[1]/div[1]/h3/span").text
            except:
                pass
            if ('_' in text):
                try:
                    Output = text.split('_')
                    a = passage.find(Output[0])
                    b = passage.find((Output[len(Output) - 1]))
                    r = range((b - a) - len(Output[0]))
                    answer = ''
                    for n in r:
                        answer = answer + passage[n + a + len(Output[0])]
                except:
                    print('idk just crashed')
            else:
                try:
                    tpy = driver.find_element('xpath', f"/html/body/div/div/form/div[{q}]/div[1]/div[1]/h3/span/b").text
                    answer = pinyin.get(tpy)
                except:
                    ('stop crashing')
            qcount = len(driver.find_elements('xpath', f"/html/body/div/div/form/div[{q}]/div[2]/table/tbody/tr"))
            for a in range(1, qcount + 1):
                optext = driver.find_element('xpath',
                                             f"/html/body/div/div/form/div[{q}]/div[2]/table/tbody/tr[{a}]/td[2]").text
                optext = (remove(optext, " "))
                opt = driver.find_element('xpath',
                                          f"/html/body/div/div/form/div[{q}]/div[2]/table/tbody/tr[{a}]/td[1]/input")
                if answer == optext:
                    opt.click()
        submit = driver.find_element('xpath', f"/html/body/div/div/form/div[{count}]/input")
        submit.click()
    except:
        pass
    startpost += 1


while True:
    try:
        driv = initDriver()
        Login(driv)
        while (True):
            DoQuiz(driv)
            print(startpost)
            with open("zbbot.txt", "w") as txt:
                txt.write(str(startpost))
    except:
        pass
"""


"""
def init():
    length = 0
    initstring = ""
    print(initstring)
    driver.get("https://www.zbschools.sg/")
    link = str(WaitTill("html/body/div/div/div/div/div/div[3]/div/div[2]/div/div/div[2]/div[1]/div/a").get_attribute("href"))
    for match in re.findall("\d*", link):
        if match != "":
            length = match
    for i in range(int(length)):
        initstring = initstring + "0\n"
    with open("zbbot.txt", "w") as txt:
        txt.write(initstring)
#Run this function when u started macroing
#uncomment the comment below
#init()
"""
