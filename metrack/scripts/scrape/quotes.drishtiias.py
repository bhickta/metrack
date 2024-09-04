# from metrack.api.scraping.core.scraper import selenium, By

# url = "https://byjus.com/free-ias-prep/useful-quotes-for-upsc-mains-exam-gs-and-essay-papers/"
# try:
#     driver, wait = selenium.get_driver_wait()
#     driver.get(url)
#     elements = driver.find_elements(By.CLASS_NAME, 'table')
#     elements_with_both_classes = [elem for elem in elements if 'table-bordered' in elem.get_attribute('class')]
#     for elem in elements_with_both_classes:
#         print(elem.text)
# except Exception as e:
#     pass