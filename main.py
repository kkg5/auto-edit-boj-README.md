import asyncio
import requests
from PySide6.QtWidgets import QApplication, QMainWindow
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import function
from mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.progressBar.setVisible(False)

        self.setGeometry(800, 300, 300, 179)

        for v in el:
            self.comboBox.addItem(v)

        self.pushButton.clicked.connect(self.edit)
        self.pushButton_2.clicked.connect(self.examine)

    def edit(self):

        self.name = []
        self.num = []
        self.difficulty = []

        self.text = ''
        self.link = ''
        self.content = ''

        self.label_2.setText('editing..')
        self.progressBar.setVisible(True)
        self.progressBar.setValue(0)

        index = self.comboBox.currentIndex() + START_INDEX

        driver = webdriver.Chrome(service=Service(
            './chromedriver'), options=options)
        driver.get('https://www.acmicpc.net/step')
        driver.find_element(By.CSS_SELECTOR, 'body > div.wrapper > div.container.content > div:nth-child(5) '
                                             '> div > div > table > tbody > '
                                             f'tr:nth-child({index}) > td:nth-child(2) > a').click()

        req = driver.page_source

        driver.close()

        soup = BeautifulSoup(req, 'html.parser')
        self.num = []
        for v in soup.select('.list_problem_id'):
            self.num.append(v.getText())

        progress_value = 100 / len(self.num)
        cur_value = 0

        for n in self.num:
            webpage = requests.get(f'https://solved.ac/search?query={n}')
            soup = BeautifulSoup(webpage.content, 'html.parser')

            self.difficulty.append(soup.img.__getitem__(key='src'))

            v = soup.select('.__Latex__')

            self.name.append(v[0].getText())

            cur_value += progress_value
            self.progressBar.setValue(cur_value)

        asyncio.run(function.build_str(self))

    def examine(self):
        asyncio.run(function.examine(self))


options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--window-size=1024,768')
options.add_argument('--disable-gpu')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(
    './chromedriver'), options=options)
driver.get('https://www.acmicpc.net/step')

el = []

START_INDEX = 1

for i in range(START_INDEX, 51):
    el.append(driver.find_element(By.CSS_SELECTOR,
                                  f'body > div.wrapper > div.container.content > div:nth-child(5) > '
                                  f'div > div > table > tbody > tr:nth-child({i}) > td:nth-child(2) > a').text)

driver.close()

app = QApplication()
window = MainWindow()
window.show()
app.exec()
