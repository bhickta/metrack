import frappe
import re

def execute():
    fields = ['name', 'question', 'a', 'b', 'c', 'd', 'e', 'f', 'explanation']
    all_mcqs = frappe.get_all("MCQ", fields=fields)

    updates_batch = []
    print(len(all_mcqs))
    for mcq in all_mcqs:
        updates = {}
        for field in fields:
            value = mcq.get(field)
            if not value:
                continue
            cleaned_value = clean_whitespace(value)
            if cleaned_value != value:
                updates[field] = cleaned_value

        if updates:
            updates_batch.append((mcq['name'], updates))

        if len(updates_batch) >= 1000:
            batch_update(updates_batch)
            updates_batch = []

    if updates_batch:
        batch_update(updates_batch)
        print("Updated {} MCQs".format(len(updates_batch)))


def batch_update(updates_batch):
    for mcq_name, updates in updates_batch:
        frappe.db.sql("""
            UPDATE `tabMCQ`
            SET {}
            WHERE name = %s
        """.format(", ".join([f"`{field}` = %s" for field in updates])),
        tuple(updates.values()) + (mcq_name,))

    frappe.db.commit()

def clean_whitespace(text):
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\t+', '\t', text)
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\r+', '\r', text)
    
    return text