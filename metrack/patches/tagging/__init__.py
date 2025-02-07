
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

def reset_mcq_tags():
    """Set `_user_tags` to NULL in `tabMCQ` table."""
    frappe.db.sql("UPDATE `tabMCQ` SET _user_tags = NULL;")
    frappe.db.commit()

def delete_all_tags():
    """Delete all records from `tabTags` table."""
    frappe.db.sql("DELETE FROM `tabTags`;")
    frappe.db.commit()