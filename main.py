from PySide6.QtWidgets import QApplication, QMainWindow
from bs4 import BeautifulSoup

from mainwindow import Ui_MainWindow
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.name = []
        self.num = []
        self.difficulty = []
        self.setupUi(self)
        for v in el:
            self.comboBox.addItem(v)
        self.pushButton.clicked.connect(self.button_clicked)
        self.text = ''
        self.link = ''
        self.content = ''

    def button_clicked(self):
        index = self.comboBox.currentIndex() + 1
        driver = webdriver.Chrome(service=Service('./chromedriver'))
        driver.set_window_rect(0, 0, 0, 0)
        driver.get('https://www.acmicpc.net/step')
        driver.find_element(By.CSS_SELECTOR, 'body > div.wrapper > div.container.content > div:nth-child(5) > div > '
                                             f'div > table > tbody > tr:nth-child({index}) > td:nth-child(2) > a').click()

        req = driver.page_source

        soup = BeautifulSoup(req, 'html.parser')
        self.num = []
        for v in soup.select('.list_problem_id'):
            self.num.append(v.getText())

        for n in self.num:
            driver.get(f'https://solved.ac/search?query={n}')
            req = driver.page_source
            soup = BeautifulSoup(req, 'html.parser')
            v = soup.select('#__next > div.contents > div:nth-child(4) > div:nth-child(2) > div > '
                            'div.StickyTable__Wrapper-sc-45ty5n-3.cerLvn.sticky-table > div > div:nth-child(2) > '
                            'div:nth-child(1) > span > a > img')
            self.difficulty.append(v[0].__getitem__(key='src'))
            v = soup.select('#__next > div.contents > div:nth-child(4) > div:nth-child(2) > div > '
                            'div.StickyTable__Wrapper-sc-45ty5n-3.cerLvn.sticky-table > div > div:nth-child(2) > '
                            'div:nth-child(2) > span > a > span')
            self.name.append(v[0].getText())

        self.text += '\n---\n\n### ' + self.comboBox.currentText() + '\n\n| 난이도 | 번호 | 이름 | 날짜 | 체크 ' \
                                                                  '|\n|:---:|:---:|:---:|:---:| :---: |\n '
        self.link += '\n'

        for a in range(len(self.num)):
            self.text += f'| <img src="{self.difficulty[a]}" width="20px" height="25px"></img> | [{self.num[a]}][{self.num[a]}] | {self.name[a]} |  |  |\n '
            self.link += f'[{self.num[a]}]: https://www.acmicpc.net/problem/{self.num[a]}\n'
        self.content += f'| [{self.comboBox.currentText()}](#{self.comboBox.currentText().replace(", ", "-").replace(" ", "-")}) |\n'
        self.edit()

    def edit(self):
        with open('README1.md', 'r') as f:
            lines = f.readlines()
        with open('README2.md', 'w') as f:
            for line in lines:
                if line.rstrip() == '<!-- Contents -->':
                    f.write(self.content)
                    f.write('<!-- Contents -->\n')
                elif line.rstrip() == '<!-- ### -->':
                    f.write(self.text)
                    f.write('<!-- ### -->\n')
                else:
                    f.write(line)
            f.write(self.link)


driver = webdriver.Chrome(service=Service('./chromedriver'))
driver.set_window_rect(0, 0, 0, 0)
driver.get('https://www.acmicpc.net/step')
el = []

for i in range(1, 51):
    el.append(driver.find_element(By.CSS_SELECTOR, f'body > div.wrapper > div.container.content > div:nth-child(5) > div > div > table > tbody > tr:nth-child({i}) > td:nth-child(2) > a').text)
driver.close()

app = QApplication()
window = MainWindow()
window.show()
app.exec()
