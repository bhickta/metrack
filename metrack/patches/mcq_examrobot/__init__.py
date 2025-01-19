import frappe
json = frappe.json

def execute():
    frappe.db.sql("DELETE FROM `tabMCQ`")
    data = frappe.get_doc("File", {"file_url": "/files/examrobot.json"}).get_content()
    questions = json.loads(data)
    for question in questions:
        doc = frappe.new_doc("MCQ")
        value_key_map = {
            "1": "a",
            "2": "b",
            "3": "c",
            "4": "d",
            "5": "e",
            "6": "f",
        }
        new_question = {
            "question": question.get("question"),
            "subject": question.get("subject"),
            "metadata": str(question.get("metadata")),
            "answer": value_key_map.get(question.get("correct_option")),
            "explanation": question.get("explanation"),
            "source": "Examrobot",
        }
        options = question.get("options")
        if options:
            for i in range(len(options)):
                key = value_key_map.get(str(i + 1))
                new_question[key] = options[i].get("label")
        doc.update(new_question)
        doc.save()