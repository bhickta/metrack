
import frappe
def execute():
    from metrack.api.tagging.fais import set_tags as _set_tags
    mcqs = frappe.get_all("MCQ", pluck="name")
    total = len(mcqs)
    for idx, mcq in enumerate(mcqs):
        print((idx/total)*100, idx)
        doc = frappe.get_doc('MCQ', mcq)
        _set_tags(doc)
        for tag in doc.ranked_tags:
            doc.tags = []
            doc.append("tags", {
                "syllabus_theme": tag.get("meta", {}).get("origin_name"),
                "rank": float(tag.get("tag", ("tag", 0))[1]),
            })
            doc.save()
            frappe.db.commit()