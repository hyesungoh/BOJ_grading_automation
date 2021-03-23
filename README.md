## BOJ grading automation

백준 채점 자동화 프로그램

### Development tool

> <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white"/> <img src="https://img.shields.io/badge/Selenium-43B02A?style=flat-square&logo=Selenium&logoColor=white"/>

### Result

#### [Youtube Link](https://youtu.be/jMBtbVg0Abw)

Selenium을 이용하여 동적 크롤링

![스크린샷 2021-03-24 오전 1 07 14](https://user-images.githubusercontent.com/26461307/112181418-c7550c00-8c3f-11eb-87e3-271008b5f301.png)

채점결과 CSV 파일로 저장

![스크린샷 2021-03-24 오전 1 08 18](https://user-images.githubusercontent.com/26461307/112181432-ca4ffc80-8c3f-11eb-845d-4d7cc88318f2.png)

### Develop Log

-   `이름(학번), 백준 ID`로 이루어진 CSV 파일을 읽어 딕셔너리화하여 반환

```python
def return_student_information():
    file = open(CSV_FILE_NAME, "r", encoding='utf-8')
    reader = csv.reader(file)

    student_information = {}
    for line in reader:
        if line[0] == "성명": continue
        student_information[line[0]] = line[1]

    file.close()
    # student_information = {"오혜성": "hs980414", "한슬희": "3021062"}
    return student_information
```

-   백준 ID를 이용해 백준 프로필로 이동 후 주차별 통과 여부, 각 문제별 풀었는 지 확인하여 반환

```python
def grading(student_id, problems):
    driver.get(BOJ_URL + student_id)
    page_source = BeautifulSoup(driver.page_source, "html.parser")s

    correct_div = page_source.find("div", {"class": "panel-body"})
    students_answers = []
    for answer in correct_div.findAll("a"):
        students_answers.append(answer.get_text())

    is_passed = 'O'
    is_solve_by_problems = []

    for problem in problems:
        if problem not in students_answers:
            is_passed = 'X'
            is_solve_by_problems.append('X')
        else: is_solve_by_problems.append('O')

    return [is_passed, is_solve_by_problems]
```

-   성명, 백준 ID, 제출 결과, 각 문제별 결과를 CSV 파일로 저장

```python
def write_csv():
    def write_base():
        csv_infomation = current_date + "/" + problems[0] + "/" + problems[1]
        writer.writerow([csv_infomation])
        writer.writerow(["성명", "백준 ID", "제출 결과"] + problems)

    problems = input("이번 주 제출 문제 '공백으로 나누어' 입력하세요 : ").split()
    file = open(GRADING_FILE_NAME, "w", newline='')
    writer = csv.writer(file)
    write_base()

    students_information = return_student_information()
    total_students_length = len(students_information)

    for index, student_information in enumerate(students_information.items()):
        student_name, student_id = student_information

        if student_id == "미제출":
            writer.writerow([student_name, "ID 미제출"])
        else:
            is_passed, is_solve_by_problems = grading(student_id, problems)
            writer.writerow([student_name, student_id, is_passed] + is_solve_by_problems)
        print("%d / %d ------- %s 학생 : %s" %(index+1, total_students_length, student_name, is_passed))
    file.close()

```

### Issue

-   Selenium chrome driver version
    -   로컬 [chrome 버전에 맞는 driver](https://chromedriver.chromium.org/downloads)을 업데이트하여 수정

### Extend

-   LMS상 채점을 자동화
    -   LMS 제출 결과에 "면접"이 있을 시 만점 처리
    -   채점 로그 작성
