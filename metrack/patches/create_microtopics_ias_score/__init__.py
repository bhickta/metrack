import frappe

import frappe.public

def execute():
    # Get file details
    file_doc = frappe.get_doc("File", {"file_url": "/files/microtopics.json"})
    microtopics = frappe.parse_json(file_doc.get_content())
    
    # Process each key and create documents
    for key in ["subject", "section", "topic", "theme", "subtheme"]:
        doctype = key.title()
        
        # Use a set to store unique, non-empty entries
        entries = {entry.get(key, "").strip() for entry in microtopics if entry.get(key)}
        
        # Create or skip documents for each entry
        for entry in entries:
            entry = entry.strip()  # Remove any extra spaces
            if entry and not frappe.db.exists(doctype, {"title": entry[:140]}):  # Check for duplicates
                frappe.get_doc({
                    "doctype": doctype,
                    "title": entry[:140]
                }).insert()
    for theme in microtopics:
        doc = frappe.new_doc("Syllabus Theme")
        new_theme = {
            "subject": theme.get("subject"),
            "section": theme.get("section"),
            "topic": theme.get("topic"),
            "theme": theme.get("theme")[:140],
            "subtheme": theme.get("subtheme", "")[:140],
        }
        doc.update(new_theme)
        doc.save()