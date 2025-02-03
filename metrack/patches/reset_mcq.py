import frappe

def execute():
    query = """
    DELETE FROM `tabMCQ`
    WHERE source LIKE '%insights%'
    """
    
    frappe.db.sql(query)