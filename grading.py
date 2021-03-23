from selenium import webdriver
from bs4 import BeautifulSoup
import csv

CSV_FILE_NAME = "boj_id_csv.csv"
GRADING_FILE_NAME = "grading.md"
BOJ_URL = "https://www.acmicpc.net/user/"

def return_student_information():
    file = open(CSV_FILE_NAME, "r", encoding='utf-8')
    reader = csv.reader(file)

    student_information = {}
    for line in reader:
        if line[0] == "성명": continue
        student_information[line[0]] = line[1]

    file.close()
    return student_information

def grading(student_id, problems):
    driver.get(BOJ_URL + student_id)
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

    
driver = webdriver.Chrome('chromedriver')
problems = input().split()
# student_information = return_student_information()
grading("hs980414", problems)

