import os
import requests
import frappe
from metrack.controllers.search_controller import meilisearch

meilisearch_client = meilisearch.Client("http://meilisearch:7700")

def execute():
    directory = "prelims"
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_url_map = {
        "Prelims 2015": "https://raw.githubusercontent.com/project-ias/project-ias/master/backend/pyq_scrapers/prelims2015.json",
        "Prelims 2016": "https://raw.githubusercontent.com/project-ias/project-ias/master/backend/pyq_scrapers/prelims2016.json",
        "Prelims 2017": "https://raw.githubusercontent.com/project-ias/project-ias/master/backend/pyq_scrapers/prelims2017.json",
        "Prelims 2018": "https://raw.githubusercontent.com/project-ias/project-ias/master/backend/pyq_scrapers/prelims2018.json",
        "Prelims 2019": "https://raw.githubusercontent.com/project-ias/project-ias/master/backend/pyq_scrapers/prelims2019.json",
        "Prelims 2020": "https://raw.githubusercontent.com/project-ias/project-ias/master/backend/pyq_scrapers/prelims2020.json",
    }

    try:
        for source, file_url in file_url_map.items():
            response = requests.get(file_url)
            response.raise_for_status()

            file_path = os.path.join(directory, f"{source.replace(' ', '_').lower()}.json")
            if not os.path.exists(file_path):
                with open(file_path, 'w') as file:
                    file.write(response.text)

            with open(file_path, 'r') as file:
                data = file.read()

            import_mcqs(data, source)

        frappe.db.commit()
    except Exception as e:
        frappe.db.rollback()
        raise e

def import_mcqs(data, source):
    data = frappe.parse_json(data)
    for mcq in data.get("prelims", []):
        question_text = mcq.get("question")
        options = mcq.get("options")
        answer = mcq.get("answer")
        explanation = mcq.get("explanation")

        if not frappe.db.exists("MCQ", {"question": question_text.strip()}):
            mcq_doc = frappe.get_doc({
                "doctype": "MCQ",
                "question": question_text.strip(),
                "a": options[0],
                "b": options[1],
                "c": options[2],
                "d": options[3],
                "answer": answer.strip().split(')')[0][-1],
                "explanation": explanation,
                "source": source,
            })
            mcq_doc.insert()