
import frappe
def execute():
    from metrack.api.tagging.fais import set_tags as _set_tags
    mcqs = frappe.get_all("MCQ", pluck="name", filters={"syllabus_theme": ["is", "not set"]})
    total = len(mcqs)
    for idx, mcq in enumerate(mcqs):
        print(f"({(idx/total)* 100:.2f}), remaining: {total - idx}")
        doc = frappe.get_doc('MCQ', mcq)
        _set_tags(doc)
        doc.tags = []
        for tag in doc.ranked_tags:
            doc.append("tags", {
                "syllabus_theme": tag.get("meta", {}).get("origin_name"),
                "rank": float(tag.get("tag", ("tag", 0))[1]),
            })
            doc.save()
            frappe.db.commit()

def clean_tags():
    query_1 = f"""
        UPDATE
            `tabMCQ` m
        SET
            m._user_tags = NULL;
    """
    
    query_2 = f"""
        DELETE FROM `tabTags`;
    """
    
    for query in [query_1, query_2]:
        frappe.db.sql(query)
    frappe.db.commit()