import re
import requests
from PySide6.QtWidgets import QApplication, QMainWindow
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.name = []
        self.num = []
        self.difficulty = []

        self.text = ''
        self.link = ''
        self.content = ''

        self.progressBar.setVisible(False)

        self.setGeometry(800, 300, 300, 179)

        for v in el:
            self.comboBox.addItem(v)

        self.pushButton.clicked.connect(self.edit)
        self.pushButton_2.clicked.connect(self.examine)

    def edit(self):

        self.label_2.setText('editing..')
        self.progressBar.setVisible(True)
        self.progressBar.setValue(0)

        index = self.comboBox.currentIndex() + START_INDEX

        driver = webdriver.Chrome(service=Service('./chromedriver.exe'))
        driver.set_window_rect(0, 0, 0, 0)
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

            v = soup.select('div.ProblemTitleTag__ProblemTitle-sc-iphdox-1.kihrnS > a > span')

            self.name.append(v[0].getText())

            cur_value += progress_value
            self.progressBar.setValue(cur_value)

        self.build_str()
        self.write()

    def build_str(self):

        self.text += '\n---\n\n### ' + self.comboBox.currentText() + '\n\n| 난이도 | 번호 | 이름 | 날짜 | 체크 ' \
                                                                     '|\n|:---:|:---:|:---:|:---:| :---: |\n '
        self.link += '\n'

        for a in range(len(self.num)):
            self.text += f'| <img src="{self.difficulty[a]}" width="20px" height="25px"></img> ' \
                         f'| [{self.num[a]}][{self.num[a]}] | {self.name[a]} |  |  |\n'
            self.link += f'[{self.num[a]}]: https://www.acmicpc.net/problem/{self.num[a]}\n'

        self.content += f'| [{self.comboBox.currentText()}]' \
                        f'(#{self.comboBox.currentText().replace(", ", "-").replace(" ", "-")}) |\n'

    def write(self):
        with open('README1.md', 'r', encoding="UTF-8") as f:
            lines = f.readlines()
        with open('README2.md', 'w', encoding="UTF-8") as f:
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

        self.label_2.setText('Success!')
        self.progressBar.setValue(100)

    def examine(self):
        with open('README1.md', 'r', encoding="UTF-8") as f:
            lines = f.readlines()

        li = []

        self.label_2.setText('examining..')
        self.progressBar.setVisible(True)
        self.progressBar.setValue(0)

        progress_value = 100 / len(lines)
        cur_value = 0

        for line in lines:
            if line.rstrip()[:48] == '| <img src="https://static.solved.ac/tier_small/':
                nums = re.findall('[0-9]+', line)
                num = nums[3]
                dif = nums[0]

                webpage = requests.get(f'https://solved.ac/search?query={num}')
                soup = BeautifulSoup(webpage.content, 'html.parser')

                difficulty = re.search('[0-9]+', soup.img.__getitem__(key='src')).group()

                if dif != difficulty:
                    li.append('(' + num + ') ' + line.split(' | ')[-3])

            cur_value += progress_value
            self.progressBar.setValue(int(cur_value))

        if not li:
            self.label_2.setText('Success! No wrong difficulty.')
        else:
            self.label_2.setText('Success!\n'
                                 'Problem:\n\t'
                                 ',\n\t'.join(li))

        self.progressBar.setValue(100)


driver = webdriver.Chrome(service=Service('./chromedriver.exe'))
driver.set_window_rect(0, 0, 0, 0)
driver.get('https://www.acmicpc.net/step')

el = []

START_INDEX = 25

for i in range(START_INDEX, 51):
    el.append(driver.find_element(By.CSS_SELECTOR,
                                  f'body > div.wrapper > div.container.content > div:nth-child(5) > '
                                  f'div > div > table > tbody > tr:nth-child({i}) > td:nth-child(2) > a').text)

driver.close()

app = QApplication()
window = MainWindow()
window.show()
app.exec()
