import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import json
import os
import sys


class Findindg(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path= '/usr/bin/chromedriver')
        self.filename = sys.argv[1]
        self.new_filename = self.filename.split('.')[0]
        self.driver.get("file://" + os.path.abspath(os.getcwd())+"/"+self.filename)
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(5)
        self.driver.implicitly_wait(15)
    
    
    def test_get_questions(self):
        questions = self.driver.find_elements_by_class_name("Question")

        resultados = []
        for index, question in enumerate(questions):
            numero_pregunta = questions[index].find_element_by_class_name('Question-count').text
            pregunta = questions[index].find_element_by_class_name('Question-item').text
            answer = questions[index].find_element_by_class_name('Question-answer').text
            is_correct="CORRECT"
            try:            
                print(index+1)
                WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR,
                     f"#exam-summary > div > div.ResultsOverview > div.u-wrapper > div:nth-child({index + 1}) > div.Question-result.Question-result--correct")
                    )
                )
            except Exception as e:
                is_correct = "INCORRECT"
            resultados.append(
                {"numero":numero_pregunta, "pregunta":pregunta, "respuesta":answer, "resultado":is_correct}
            )
        
        
        if not os.path.exists(self.filename + ".csv"): 
            csv_columns = ['numero','pregunta', 'respuesta', 'resultado']
            csv_file = self.new_filename + ".csv"
            try:
                with open(csv_file, 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=csv_columns, extrasaction='ignore')
                    writer.writeheader()
                    for data in resultados:
                        writer.writerow(data)
            except IOError:
                print("Something went wrong on the  .csv")

        if not os.path.exists(self.filename + '.json'):
            reporte = self.new_filename + '.json'    
            try:
                with open(reporte, "w") as f:
                    f.write((json.dumps(resultados)))
            except IOError:
                print("Something went wrong in the .json")



if __name__== "__main__":
    if len(sys.argv) != 2:
        print("Please supply a file name")
        raise SystemExit(1)
    unittest.main(verbosity=2, argv=['first-arg-is-ignored'])
    