# pracht_module — leere Frappe-App als Modul-Container

> **Gebaut, noch nicht installiert.** Angelegt am 2026-09-08 (K23), Remote
> `github.com/andreas-pracht/pracht_module` (**öffentlich**, K34/Weg B),
> Tag `v0.0.1`, seit dem 2026-09-08 im Custom Image enthalten.
> **Die Installation auf der Site steht aus** — eigenes Gate (K22).
> Verfahren: [`../../_briefing/erpnext-hr/07-modul-app-installation.md`](../../_briefing/erpnext-hr/07-modul-app-installation.md)

## Wozu

Diese App enthält **keine Logik**. Ihr einziger Zweck ist, die Module
`Vermietung` und `Fuhrpark` als **Dateisystem-Module** zu registrieren.

Ohne App im Dateisystem behandelt Frappe die zugehörigen Workspaces als
verwaist: Sie erscheinen nicht im Hauptmenü, sondern nur über `/app/<name>`
und Cmd+K — und eine Migration kann sie löschen. **Am 2026-07-29 ist genau das
passiert**: Die Migration auf 16.30.0 löschte den Workspace `Vermietung`
(`Deleting entity Workspace Vermietung`); er musste aus der Fixture
wiederhergestellt werden.

## 🔴 Bedingung für die öffentliche Sichtbarkeit

Dieses Repo ist **öffentlich**, damit der Build-Host es ohne Token klonen kann
(Entscheidung des Inhabers vom 2026-09-08, Weg B). Daran hängt eine Bedingung:

> **Die App bleibt ein reiner Modul-Container. Sobald Fixtures, Print Formats
> oder Firmenlogik hineinsollen, geht sie zurück auf privat**, und der Zugang
> läuft über einen Fine-grained PAT (Repository access: nur dieses Repo,
> Contents: Read-only), eingetragen in der `apps.json` **auf dem Host**.

**Wer hier Inhalt ergänzen will, prüft zuerst: Ist das etwas, das öffentlich
stehen darf?** Wenn nein, erst die Sichtbarkeit ändern, dann committen — nicht
umgekehrt. Ein Commit ist öffentlich, sobald er gepusht ist; ihn danach privat
zu stellen holt ihn nicht zurück.

Verfahren für den privaten Fall:
`platform/erpnext/_briefing/erpnext-hr/02-custom-image.md`, § 3.

## Was hier *nicht* hineingehört

DocTypes, Server Scripts, Client Scripts, Print Formats und Fixtures bleiben
**Customizing auf der Site** (`custom = 1`) und werden über
`platform/erpnext/sites/erpnext.autmation.org/fixtures/` versioniert — nicht
über diese App. Das ist [ADR-0006](../../docs/decisions/0006-customizing-strategie.md)
und bleibt so.

**Wer hier Logik ergänzt, macht aus einem Modul-Container eine Custom App** —
und damit jedes ERPNext-Update zu einem Code-Kompatibilitätsproblem. Der
Hinweis steht auch im Kopf von `hooks.py`, damit er beim Bearbeiten sichtbar
ist.

## Struktur

```
pracht_module/
├── pyproject.toml              flit-Build, Frappe/ERPNext >=16 <17
├── license.txt                 MIT
├── README.md                   diese Datei
└── pracht_module/
    ├── __init__.py             __version__ = "0.0.1"
    ├── hooks.py                app_name, required_apps, Begründung
    ├── modules.txt             Vermietung / Fuhrpark
    ├── patches.txt             leer
    ├── config/__init__.py
    ├── vermietung/__init__.py  Modulverzeichnis (scrubbed name)
    └── fuhrpark/__init__.py    Modulverzeichnis (scrubbed name)
```

Die Verzeichnisnamen unter `pracht_module/` sind die *scrubbed names* der
Einträge in `modules.txt` — kleingeschrieben, Leerzeichen zu Unterstrichen.
Bei `Vermietung` und `Fuhrpark` fallen beide zusammen.

## Was noch einzusetzen ist

| # | Stelle | Stand |
| --- | --- | --- |
| 1 | **Remote-URL** | ✅ `https://github.com/andreas-pracht/pracht_module`, in `deploy/erpnext-image/apps.json` mit Tag `v0.0.1` |
| 2 | **App-Name** | ✅ `pracht_module` bestätigt (K31). Geprüft: `bench` leitet den Namen aus `pyproject.toml` ab, nicht aus der URL — beide stimmen überein, kein Rename |
| 3 | **Installation auf der Site** | ⏳ eigenes Gate nach A2 — [`07-modul-app-installation.md`](../../_briefing/erpnext-hr/07-modul-app-installation.md) |

### Wenn der Name geändert wird

Der Name kommt an **sechs** Stellen vor. Alle in einem Zug ändern:

| Stelle | |
| --- | --- |
| Ordner `apps/pracht_module/` | äußeres Verzeichnis |
| Ordner `apps/pracht_module/pracht_module/` | inneres Verzeichnis (= Python-Paket) |
| `pyproject.toml` | `name = "…"` |
| `hooks.py` | `app_name = "…"` |
| `deploy/erpnext-image/apps.json` | Repo-URL |
| `bench install-app <name>` | im Installationsplan |

Der Name muss ein **gültiger Python-Modulname** sein: Kleinbuchstaben,
Unterstriche, keine Bindestriche.

## Verhältnis Repo ↔ Workspace-Spiegel

Nach K23 liegt der Quellcode **doppelt**: im Repo (das `apps.json`
referenziert) und hier als Spiegel.

🔴 **Diese Doppelung ist jetzt scharf.** Der Build zieht **das Repo am Tag
`v0.0.1`**, nicht diesen Ordner. Wer nur hier ändert, ändert am gebauten Image
nichts — und merkt es erst, wenn die Installation etwas anderes tut als
erwartet.

**Bei jeder Änderung deshalb beides:** hier ändern, ins Repo pushen, **neuen
Tag setzen** und den Tag in `deploy/erpnext-image/apps.json` nachziehen. Ein
Build gegen `v0.0.1` bleibt sonst auf dem alten Stand, egal was hier steht.

**Empfehlung, um die Doppelung ganz loszuwerden:** Diesen Ordner selbst zum
Arbeitsverzeichnis mit dem Remote machen (`git init` + `git remote add`), dann
ist er kein Spiegel, sondern das Original. Das wäre dieselbe Bauart wie die
drei Website-Repos (ADR-0003) und bräuchte einen Eintrag im Workspace-
`.gitignore`. **Noch nicht umgesetzt** — deine Entscheidung.
