import frappe
def get_users():
    settings = frappe.get_single("Metrack Settings")
    users = [u.user for u in settings.auto_reporting]
    return users

def execute():
    for user in get_users():
        if not frappe.db.exists("Daily Self Reporting", {"user": user, "posting_date": frappe.utils.today()}):
            doc = frappe.new_doc("Daily Self Reporting")
            doc.user = user
            doc.insert()
