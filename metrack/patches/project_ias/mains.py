import frappe
import requests
from metrack.controllers.search_controller import meilisearch
import os

meilisearch_client = meilisearch.Client("http://meilisearch:7700")

def execute():
    directory = "mains"
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_url = "https://raw.githubusercontent.com/project-ias/project-ias/master/backend/pyq_scrapers/pyqs.json"
    response = requests.get(file_url)
    response.raise_for_status()
    file_path = os.path.join(directory, f"mains.json")
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write(response.text)

    with open(file_path, 'r') as file:
        data = file.read()
    data = frappe.parse_json(data)
    import_pyqs(data)
    frappe.db.commit()


def import_pyqs(data):
    for pyq in data.get("pyqs", []):
        exam_name = pyq.get("exam")
        if not frappe.db.exists("Exam", {"title": exam_name}):
            exam_doc = frappe.get_doc({"doctype": "Exam", "title": exam_name})
            exam_doc.insert()

        topics = []
        for topic_name in pyq.get("topics", []):
            topic_name_clean = topic_name.strip()
            if not frappe.db.exists("Topic", {"title": topic_name_clean}):
                topic_doc = frappe.get_doc({"doctype": "Topic", "title": topic_name_clean})
                topic_doc.insert()
            topic_doc = frappe.get_doc("Topic", {"title": topic_name_clean})
            topics.append(topic_doc.name)

        if not frappe.db.exists("Subjective Question", {"title": pyq.get("question")}):
            question_doc = frappe.get_doc({
                "doctype": "Subjective Question",
                "title": pyq.get("question"),
                "year": pyq.get("year") if len(pyq.get("year")) < 140 else pyq.get("year")[140],
                "exam": exam_name,
            })

            for topic in topics:
                question_doc.append("subjective_question_topic", {
                    "topic": topic
                })
            question_doc.insert()
        frappe.db.commit()