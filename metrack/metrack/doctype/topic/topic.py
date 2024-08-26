# Copyright (c) 2024, nishantbhickta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests


class Topic(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        exam: DF.Link | None
        subject: DF.Link
        title: DF.SmallText | None
    # end: auto-generated types
    pass


# Function to populate the Topic document
def populate_topics_from_json(url):
    file_url = frappe.utils.get_files_path("topics_data.json")
    data = frappe.get_file_json(file_url)["children"]
    for gs in data:
        gs_name = gs["label"]
        subjects = gs["children"]
        for subject in subjects:
            subject_name = subject["label"]
            topics = subject["children"]
            questions = subject["questions"]
            for topic, question in zip(topics, questions):
                create_topics(
                    exam=gs_name, subject=subject_name, title=topic, question=question
                )


def create_topics(**kwargs):
    title = kwargs.get("title")
    subject_name = kwargs.get("subject")
    exam_name = kwargs.get("exam")
    question = kwargs.get("question")

    if not frappe.db.exists("Topic", {"title": title}):
        try:
            exam_doc = frappe.get_doc("Exam", {"title": exam_name})
        except frappe.exceptions.DoesNotExistError:
            exam_doc = frappe.get_doc(
                {"doctype": "Exam", "title": exam_name, "abbreviation": exam_name}
            )
            exam_doc.insert()

        try:
            subject_doc = frappe.get_doc("Subject", {"title": subject_name})
        except frappe.exceptions.DoesNotExistError:
            subject_doc = frappe.get_doc(
                {"doctype": "Subject", "title": subject_name, "exam": exam_doc.name}
            )
            subject_doc.insert()

        topic = frappe.get_doc(
            {
                "doctype": "Topic",
                "title": title,
                "subject": subject_doc.name,
                "exam": exam_doc.name,
            }
        )
        topic.insert()


# Main script execution
def execute():
    url = "https://raw.githubusercontent.com/project-ias/project-ias/master/backend/topics.json"
    # Connect to Frappe
    populate_topics_from_json(url)
    frappe.db.commit()
