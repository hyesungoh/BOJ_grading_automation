from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date
import csv


CSV_FILE_NAME = "boj_id_csv.csv"
current_date = date.today().strftime("%m%d")
GRADING_FILE_NAME = "채점결과_%s.csv" %current_date
BOJ_URL = "https://www.acmicpc.net/user/"

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


def grading(student_id, problems):
    driver.get(BOJ_URL + student_id)
    page_source = BeautifulSoup(driver.page_source, "html.parser")

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

driver = webdriver.Chrome('chromedriver')
write_csv()
driver.close()
