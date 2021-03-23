# rom selenium import webdriver
#
# driver = webdriver.Chrome('chromedriver')
# driver.get(URL)
# ...
#
# driver.close()


from selenium import webdriver
import csv

CSV_FILE_NAME = "boj_id_csv.csv"

def return_student_information():
    file = open(CSV_FILE_NAME, "r", encoding='utf-8')
    reader = csv.reader(file)

    student_information = {}
    for line in reader:
        if line[0] == "성명": continue
        student_information[line[0]] = line[1]

    file.close()
    return student_information


student_information = return_student_information()
print(student_information)
# driver = webdriver.Chrome('chromedriver')
# driver.get("https://www.naver.com")

