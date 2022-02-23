## auto-edit-boj-README.md

![preview](./preview.png)

파이썬 selenium, BeautifulSoup, PySide6 사용

1. [백준-단계별로 풀어보기](https://www.acmicpc.net/step)에서 "목차"를 크롤링해 comboBox에 저장
2. comboBox에 저장된 목차 중 하나를 선택해 Edit 버튼을 클릭
3. [백준-단계별로 풀어보기](https://www.acmicpc.net/step)에서 목차에 해당하는 "문제 번호"와 "이름"을 크롤링
4. [solved.ac](https://solved.ac/)에서 문제들의 "난이도"를 크롤링
5. README1.md 파일에 내용을 추가해 README2.md 파일로 저장

## Chrome Driver

https://sites.google.com/chromium.org/driver

selenium을 사용하기 위해 크롬 버전에 맞는 크롬 드라이버가 필요함

## Release Note

* 2022-02-16
  * 기본 기능

* 2022-02-21
  * progressBar 추가
  * 위치 변경
