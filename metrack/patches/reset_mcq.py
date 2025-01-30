import frappe

def execute():
    query = """
    UPDATE `tabMCQ` 
    SET `question_status` = NULL, `result` = NULL
    WHERE source LIKE '%insights%'
    """

    frappe.db.sql(query)