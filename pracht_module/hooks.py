app_name = "pracht_module"
app_title = "Pracht Module"
app_publisher = "Pracht"
app_description = "Registriert die Module Vermietung und Fuhrpark im Dateisystem"
app_email = "ai@autmation.org"
app_license = "MIT"

# Diese App enthaelt bewusst KEINE Logik.
#
# Ihr einziger Zweck ist, die Module `Vermietung` und `Fuhrpark` als
# Dateisystem-Module zu registrieren. Ohne App im Dateisystem behandelt Frappe
# die zugehoerigen Workspaces als verwaist: Sie erscheinen nicht im Hauptmenue,
# und eine Migration kann sie loeschen -- am 2026-07-29 ist genau das mit dem
# Workspace `Vermietung` passiert.
#
# DocTypes, Server Scripts, Client Scripts, Print Formats und Fixtures bleiben
# Customizing auf der Site (custom=1) und werden ueber
# platform/erpnext/sites/erpnext.autmation.org/fixtures/ versioniert -- NICHT
# ueber diese App. Das ist ADR-0006 (Customizing-as-Code) und bleibt so.
#
# Wer hier Logik ergaenzt, macht aus einem Modul-Container eine Custom App und
# damit jedes ERPNext-Update zu einem Code-Kompatibilitaetsproblem.

required_apps = ["frappe/erpnext"]
