import frappe
import csv

def execute():
    frappe.db.sql("Delete from `tabSubjective Question` where metadata is not null")
    data = frappe.get_doc("File", {"file_url": "/files/pyq_2025_krushna.csv"}).get_content()
    reader = csv.reader(data.splitlines())
    next(reader)
    
    for row in reader:
        section = row[0]
        topic = row[1]
        question_no = row[2]
        question = row[3]
        subjective_question = frappe.get_doc({
            "doctype": "Subjective Question",
            "title": question,
            "metadata": {
                "question_no": question_no,
                "section": section,
                "topic": topic,
            }
        })
        subjective_question.save()
    frappe.db.commit()