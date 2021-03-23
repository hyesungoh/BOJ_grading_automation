from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date
import csv


CSV_FILE_NAME = "boj_id_csv.csv"
current_data = date.today().strftime("%m%d")
GRADING_FILE_NAME = "채점결과_%s.csv" %current_data
BOJ_URL = "https://www.acmicpc.net/user/"

def return_student_information():
    # file = open(CSV_FILE_NAME, "r", encoding='utf-8')
    # reader = csv.reader(file)

    # student_information = {}
    # for line in reader:
    #     if line[0] == "성명": continue
    #     student_information[line[0]] = line[1]
    #
    # file.close()
    student_information = {"오혜성": "hs980414", "한슬희": "3021062"}
    return student_information

def grading(student_id, problems):
    checking_url = BOJ_URL + student_id
    driver = webdriver.Chrome('chromedriver')
    driver.get(checking_url)
    page_source = BeautifulSoup(driver.page_source, "html.parser")
    driver.close()

    correct_div = page_source.find("div", {"class": "panel-body"})
    students_answers = []
    for answer in correct_div.findAll("a"):
        students_answers.append(answer.get_text())

    for problem in problems:
        if problem not in students_answers:
            return False
    return True

def write_csv():
    def write_base():
        writer.writerow([current_data] + problems + ["제출 결과"])

    problems = input().split()
    file = open(GRADING_FILE_NAME, "w", newline='')
    writer = csv.writer(file)
    write_base()

    students_information = return_student_information()
    for student_name, student_id in students_information.items():
        isPassed = "O" if grading(student_id, problems) else "X"
        writer.writerow([student_name, student_id, isPassed])
    file.close()

write_csv()
