import frappe
import requests
import json

def execute():
    # Fetch the data from the URL
    file_url = "https://raw.githubusercontent.com/project-ias/project-ias/master/backend/pyq_scrapers/pyqs.json"
    response = requests.get(file_url)
    data = response.json()
    import_pyqs(data)
    frappe.db.commit()


def import_pyqs(data):
    for pyq in data.get("pyqs", []):
        # Ensure the Exam exists or create a new one
        exam_name = pyq.get("exam")
        if not frappe.db.exists("Exam", {"title": exam_name}):
            exam_doc = frappe.get_doc({"doctype": "Exam", "title": exam_name})
            exam_doc.insert()

        # Ensure each Topic exists or create new ones
        topics = []
        for topic_name in pyq.get("topics", []):
            topic_name_clean = topic_name.strip()
            if not frappe.db.exists("Topic", {"title": topic_name_clean}):
                topic_doc = frappe.get_doc({"doctype": "Topic", "title": topic_name_clean})
                topic_doc.insert()
            topic_doc = frappe.get_doc("Topic", {"title": topic_name_clean})
            topics.append(topic_doc.name)

        # Create the Subjective Question and link it to Exam and Topics
        if not frappe.db.exists("Subjective Question", {"title": pyq.get("question")}):
            question_doc = frappe.get_doc({
                "doctype": "Subjective Question",
                "title": pyq.get("question"),
                "year": "2024",
                "exam": exam_name,
            })

            # Add topics to the child table of the Subjective Question
            for topic in topics:
                print(topic)
                question_doc.append("subjective_question_topic", {
                    "topic": topic
                })
            # Insert the Question
            question_doc.insert()

        frappe.db.commit()