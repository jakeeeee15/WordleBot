from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder

driver = webdriver.Chrome()
driver.get(r'https://wordplay.com/new')
driver.implicitly_wait(5)

def board_type(s, keys):
    for i in s:
        keys[i].click()
    keys["ENTER"].click()

def give_path(row, col):
     return '/html/body/div/div[1]/div[1]/div/div[1]/div[2]/div/div/div[' + str(row) + ']/div[' + str(col) +']/div/div[2]'

def cutoff(words, letter, state, colu):
    print("col = " + str(colu) + " Letter : " + letter)
    ans = list()
    if state[0] == 'a':
        for word in words:
            if letter not in word:
                ans.append(word)
    elif state[0] == 'p':
        for word in words:
            if letter in word and word[colu] != letter:
                # print("FOUND")
                ans.append(word)
    elif state[0] == 'c':
        for word in words:
            # print("WORD : " + word +" len : " + str(len(word)))
            try:
                if word[colu] == letter:
                    ans.append(word)
            except:
                print("Error at " + word)


    return ans


time.sleep(2)
print("OK")
def get_keyboard():
    board = driver.find_elements(By.XPATH, r'/html/body/div/div[1]/div[1]/div/div[2]/div/div/div[1]/button')
    board = board + driver.find_elements(By.XPATH, r'/html/body/div/div[1]/div[1]/div/div[2]/div/div/div[2]/button')
    board += driver.find_elements(By.XPATH, r'/html/body/div/div[1]/div[1]/div/div[2]/div/div/div[3]/button')

    keys = dict()
    for i in board:
        keys[i.text] = i
    print(len(board))
    return keys

words = list()
with open('valid_solutions.txt', 'r') as file:
    text = file.read()
    words = text.split('\n')

words.pop(0)


row = 1

def check(s, row, words, keys):
    board_type(s, keys)
    time.sleep(4)
    for col in range(1,6):
        out = driver.find_element(By.XPATH, give_path(row, col)).get_attribute("class")
        out = out.split('-')[-1]

        words = cutoff(words, s[col-1].lower(), out, col-1)
        print(len(words))
        # print(words)
    return words

def solve(words, row, keys):
    words = check("STARE", row, words, keys)
    row+=1
    words = check("MOULD", row, words, keys)

    for i in range(1, 5):
        try:
            words = check(words[0].upper(), row+i, words, keys)
        except:
            print("The ans is " + words[0])

    # time.sleep(1000)

while True:
    print("STARting")
    keys = get_keyboard()
    solve(words, 1, keys)
    print("ENd")
    time.sleep(3)
    driver.find_element(By.XPATH, r'/html/body/div/header/div/div/button[1]').click()
    time.sleep(5)
