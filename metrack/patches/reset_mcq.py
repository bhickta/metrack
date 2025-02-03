import frappe

def execute():
    reset_mcq()

def reset_mcq():
    query = """
    UPDATE tabMCQ 
    SET question_status = NULL, result = NULL
    WHERE source LIKE '%insights%'
    """

    frappe.db.sql(query)

def delete_mcq():
    query = """
    DELETE FROM `tabMCQ`
    WHERE source LIKE '%insights%'
    """
    
    frappe.db.sql(query)