import frappe

def execute():
    query = """
    UPDATE `tabMCQ` 
    SET `question_status` = NULL, `result` = NULL;
    WHERE source like 'insights'
    """

    frappe.db.sql(query)