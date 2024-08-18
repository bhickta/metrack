from metrack.api.scraping.core import (
    selenium, BeautifulSoup, By, EC
)

class InsightDailyQuiz:
    def __init__(self) -> None:
        self.base_url = 'https://www.insightsonindia.com/'
        self.post_init()
    
    def post_init(self):
        self.url = self.base_url + '2024/07/09/upsc-static-quiz-environment-09-july-2024/'
        self.driver, self.wait = selenium.get_driver_wait()



try:
    driver, wait = selenium.get_driver_wait()
    driver.get(url)

    # Click on the start quiz button
    start_quiz_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.wpProQuiz_button[name="startQuiz"]'))
    )
    driver.execute_script("arguments[0].click();", start_quiz_button)
    
    quiz_summary_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.wpProQuiz_button[name="checkSingle"]'))
    )
    driver.execute_script("arguments[0].click();", quiz_summary_button)

    # Wait for the finish button and scroll into view
    finish_button = wait.until(
        EC.element_to_be_clickable((By.NAME, "endQuizSummary"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", finish_button)

    # Close or dismiss any interfering element
    try:
        interfering_element = driver.find_element(By.ID, "onesignal-slidedown-container")
        close_button = interfering_element.find_element(By.CSS_SELECTOR, 'button.close')
        close_button.click()
    except Exception as e:
        print("No interfering element found:", e)

    # Click on the finish quiz button using JavaScript
    driver.execute_script("arguments[0].click();", finish_button)
    
    reshow_quiz_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.wpProQuiz_button[name="reShowQuestion"]'))
    )
    driver.execute_script("arguments[0].click();", reshow_quiz_button)

    # Now scrape the quiz summary
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    questions = soup.find_all('div', class_='wpProQuiz_question')

    # Loop through each question and extract the details
    for question in questions:
        question_text = question.find('div', class_='wpProQuiz_question_text').get_text(strip=True)
        options = question.find_all('li', class_='wpProQuiz_questionListItem')
        correct_answers = question.find_all('li', class_='wpProQuiz_answerCorrect')

        # Print the question
        print('Question:', question_text)

        # Print the options
        for option in options:
            option_text = option.get_text(strip=True)
            print('Option:', option_text)

        # Print the correct answers
        for answer in correct_answers:
            correct_answer_text = answer.get_text(strip=True)
            print('Correct Answer:', correct_answer_text)

        print('---')

finally:
    driver.quit()