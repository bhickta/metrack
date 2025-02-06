import frappe

def execute():
    syllabus_themes = frappe.get_all("Syllabus Theme", filters={"subtheme": ("is", "set")}, fields="name", pluck="name")
    themes_to_delete = set()
    for syllabus_theme in syllabus_themes:
        st = frappe.get_doc("Syllabus Theme", syllabus_theme)
        subtheme = (st.theme + " :- " + st.subtheme)[0:140]
        themes_to_delete.add(st.theme)
        if frappe.db.exists("Theme", subtheme):    
            new_theme = frappe.get_doc("Theme", subtheme)
        else:
            new_theme = frappe.new_doc("Theme")
            new_theme.title = subtheme
            new_theme.save()
        new_st = frappe.copy_doc(st)
        new_st.theme = new_theme.name
        new_st.save()
        st.delete()
    frappe.db.sql("delete from `tabTheme` where name in %s", (tuple(themes_to_delete),))