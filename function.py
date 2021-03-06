import re
import requests
from bs4 import BeautifulSoup


async def build_str(self):
    self.text += '\n---\n\n### ' + self.comboBox.currentText() + '\n\n| 난이도 | 번호 | 이름 | 날짜 | 체크 ' \
                                                                 '|\n|:---:|:---:|:---:|:---:| :---: |\n '
    self.link += '\n'

    for a in range(len(self.num)):
        self.text += f'| <img src="{self.difficulty[a]}" width="20px" height="25px"></img> ' \
                     f'| [{self.num[a]}][{self.num[a]}] | {self.name[a]} |  |  |\n'
        self.link += f'[{self.num[a]}]: https://www.acmicpc.net/problem/{self.num[a]}\n'

    self.text += '\n<div align=right>\n\n[TOP](#백준boj-)\n\n</div>\n'

    self.content += f'| [{self.comboBox.currentText()}]' \
                    f'(#{self.comboBox.currentText().replace(", ", "-").replace(" ", "-")}) |\n'
    await write(self)


async def write(self):
    with open('README1.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    with open('README2.md', 'w', encoding='utf-8') as f:
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


async def examine(self):
    with open('README1.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    self.label_2.setText('examining..')
    self.progressBar.setVisible(True)
    self.progressBar.setValue(0)

    num = []
    name = {}
    dif = {}

    for line in lines:
        if line.rstrip()[:48] == '| <img src="https://static.solved.ac/tier_small/':
            nums = re.findall('[0-9]+', line)
            num.append(nums[3])
            dif[nums[3]] = nums[0]
            name[nums[3]] = line.split(' | ')[2].strip()

    num.sort(key=lambda x: int(x))

    progress_value = 100 / len(num)
    cur_value = 0

    dif2 = []
    for idx in range((len(num) - 1) // 50 + 1):
        webpage = requests.get(
            f'https://solved.ac/search?query=id:{"|".join(num[0 + 50 * idx:50 + 50 * idx])}')
        soup = BeautifulSoup(webpage.content, 'html.parser')

        soup_li = soup.select('.css-1vnxcg0')
        for idx2 in range(len(soup_li)):

            dif2.append(re.findall(
                '[0-9]+', soup_li[idx2].__getitem__(key='src'))[0])
            cur_value += progress_value
            self.progressBar.setValue(cur_value)

    wrong_li = []
    for idx in range(len(num)):
        if dif[num[idx]] != dif2[idx]:
            wrong_li.append('(' + num[idx] + ') ' + name[num[idx]])

    if not wrong_li:
        self.label_2.setText('Success! No wrong difficulty.')
    else:
        self.label_2.setText('Success!\n' +
                             'Problem:\n\t' +
                             ',\n\t'.join(wrong_li))

    self.progressBar.setValue(100)
