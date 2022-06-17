from datetime import datetime
import requests


def write(n):
    url = f'https://solved.ac/api/v3/problem/show?problemId={n}'
    response = requests.get(url)
    data = response.json()
    date = datetime.now()
    with open('README1.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    with open('README2.md', 'w', encoding='utf-8') as f:
        texts = []
        for line in lines:
            if line.rstrip() == '<!-- new -->':
                if texts[-1] == '\n':
                    texts.pop()
                texts.append(
                    f'| <img src="https://static.solved.ac/tier_small/{data["level"]}.svg" width="20px" height="25px"></img> | [{n}][{n}] | {data["titleKo"]} | {data["tags"][0]["key"]} | {date.strftime("%m/%d")} |  ✔   |')
                texts.append('\n<!-- new -->\n')
            elif line.rstrip() == '<!-- new-link -->':
                if texts[-1] == '\n':
                    texts.pop()
                texts.append(f'[{n}]: https://www.acmicpc.net/problem/{n}')
                texts.append('\n<!-- new-link -->\n')
            else:
                texts.append(line)
        f.write(''.join(texts))


while True:
    try:
        num = int(input("문제 번호를 입력해주세요: "))
        break
    except:
        print("잘못 입력되었습니다.")
        continue

write(num)

print("완료.")
