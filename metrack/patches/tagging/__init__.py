
import frappe
def execute():
    from metrack.api.tagging.fais import set_tags as _set_tags
    mcqs = frappe.get_all("MCQ", pluck="name", filters={"_user_tags": ["is", "not set"]})
    total = len(mcqs)
    for idx, mcq in enumerate(mcqs):
        print((idx/total)*100, idx)
        doc = frappe.get_doc('MCQ', mcq)
        _set_tags(doc)
        for tag in doc.tags:
            tag = frappe.db.escape(tag[0])
            tag = tag.replace(",", "")
            doc.add_tag(tag[0:140])
            frappe.db.commit()