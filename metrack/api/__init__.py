import frappe
import requests
import json

def execute():
    file_url = "https://raw.githubusercontent.com/project-ias/project-ias/master/backend/pyq_scrapers/pyqs.json"
    response = requests.get(file_url)
    data = response.json()
    questions = [questions for questions in data.values()][0]
    for question in questions:
        mcq = frappe.new_doc("MCQ")
        mcq.question = question["question"]
        options = question["options"]
        option_fields = ['a', 'b', 'c', 'd', 'e', 'f']
        for i, option in enumerate(options):
                if i < len(option_fields):
                    setattr(mcq, option_fields[i], option)
                if question['answer'] == option:
                    mcq.answer = option_fields[i]
        mcq.explanation = question['answer'] + "\n" + question["explanation"]
        mcq.source = "Prelims 2016"
        mcq.insert()
    frappe.db.commit()

import frappe

def execute():
    frappe.db.sql("""
        UPDATE `tabMCQ` SET `workflow_state` = 'Untouched';
    """)
    frappe.db.commit()