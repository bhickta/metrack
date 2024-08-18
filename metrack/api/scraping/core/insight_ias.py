from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import re
from selenium.common.exceptions import NoSuchElementException
from metrack.api.scraping.core.scraper import selenium, TimeoutException
import requests
from typing import Optional, Literal

class TypeMCQ:
    a: Optional[str] = None
    answer: Literal["", "a", "b", "c", "d", "e", "f"] = ""
    b: Optional[str] = None
    c: Optional[str] = None
    d: Optional[str] = None
    e: Optional[str] = None
    explanation: Optional[str] = None
    f: Optional[str] = None
    omr: Literal["", "a", "b", "c", "d", "e", "f"] = ""
    question: str
    question_status: Optional[str] = None
    reference: str
    source: str

class QuizScraper:
    def __init__(self):
        self.driver, self.wait = selenium.get_driver_and_wait()
    
    def ping_url(self, url):
        headers = requests.get(url).headers
        status_code = requests.get(url).status_code
        if status_code == 200:
            return True
        else:
            return False
        
    def _click_elements(self, elements):
        for by, value in elements:
            try:
                element = self.wait.until(EC.element_to_be_clickable((by, value)))
                self.driver.execute_script("arguments[0].click();", element)
            except TimeoutException as e:
                logging.warning(f"Element not found: {by} = {value}")

    def _extract_quiz_data(self, quiz_element):
        questions = quiz_element.find_elements(By.CLASS_NAME, "wpProQuiz_listItem")
        mcq_list = []
        for q in questions:
            mcq = self._parse_question(q)
            mcq_list.append(mcq)
        return mcq_list

    def _parse_question(self, question_element):
        question_text = question_element.find_element(By.CLASS_NAME, "wpProQuiz_question").text
        response_text = question_element.find_element(By.CLASS_NAME, "wpProQuiz_response").text

        correct_option = self._extract_correct_option(response_text)
        explanation = self._extract_explanation(response_text)
        reference = self._extract_reference(response_text)
        options = self._extract_options(question_text)

        mcq = TypeMCQ(
            question=re.sub(r'[a-d]\)\s[^\n]+', '', question_text).strip(),
            answer=correct_option,
            a=options.get('a'),
            b=options.get('b'),
            c=options.get('c'),
            d=options.get('d'),
            explanation=explanation,
            source="Insight IAS",
            reference=reference
        )
        return mcq

    @staticmethod
    def _extract_correct_option(response_text):
        match = re.search(r'(Ans|Answer|Solution|Sol):\s*\(?([a-d])\)?', response_text)
        return match.group(2) if match else "Not found"

    @staticmethod
    def _extract_explanation(response_text):
        match = re.search(r'Solution: \w\)\s*(.+)', response_text, re.DOTALL)
        return match.group(1).strip() if match else "Explanation not found"

    @staticmethod
    def _extract_reference(response_text):
        match = re.search(r'Refer: (.+)', response_text)
        return match.group(1).strip() if match else "Reference not found"

    @staticmethod
    def _extract_options(question_text):
        option_pattern = re.compile(r'([a-d])\)\s([^\n]+)')
        options = {match.group(1): match.group(2).strip() for match in option_pattern.finditer(question_text)}
        return options

    def scrape_quiz(self, urls: list) -> list:
        output = []
        try:
            for url in urls:
                print(url)
                if not self.ping_url(url):
                    continue
                print('scraping', url)
                self.driver.get(url)
                self._click_elements([
                    (By.ID, "onesignal-slidedown-cancel-button"),
                    (By.NAME, "startQuiz"),
                    (By.NAME, "checkSingle"),
                    (By.NAME, "endQuizSummary"),
                    (By.NAME, "reShowQuestion")
                ])
                
                quiz_set = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "wpProQuiz_quiz")))
                output.extend(self._extract_quiz_data(quiz_set))
        except NoSuchElementException as e:
            logging.error(f"NoSuchElementException: {e}")
            raise
        finally:
            self.driver.quit()

        return output