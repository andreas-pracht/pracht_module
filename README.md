# pracht_module — leere Frappe-App als Modul-Container

> **Rumpf, noch nicht in Betrieb.** Kein Git-Repo, kein Remote, nicht gebaut,
> nicht installiert. Angelegt am 2026-09-08 nach Entscheidung **K23**.
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

| # | Stelle | offen |
| --- | --- | --- |
| 1 | **Remote-URL** | Andreas legt Repo und URL fest (K23). Einzutragen in `deploy/erpnext-image/apps.json` |
| 2 | **App-Name** | `pracht_module` ist ein **Vorschlag**. Wird er geändert, siehe unten |
| 3 | **`git init`** | hier noch nicht ausgeführt |

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

Nach K23 liegt der Quellcode **doppelt**: im eigenen privaten Repo (das
`apps.json` referenziert) und hier als Spiegel.

⚠️ **Zwei Kopien können auseinanderlaufen.** Der Build zieht **das Repo**, nicht
diesen Ordner — wer nur hier ändert, ändert am gebauten Image nichts.
Empfehlung: Diesen Ordner **selbst** zum Arbeitsverzeichnis mit dem Remote
machen (`git init` + `git remote add`), statt zwei getrennte Kopien zu pflegen.
Dann ist der Spiegel kein Spiegel, sondern das Original.

Das berührt ADR-0003 (Websites = eigenes Repo) nur der Form nach: Wie bei den
drei Website-Repos läge auch hier ein eigenes Repo physisch im Workspace und
wäre in dessen `.gitignore` auszuschließen. **Ob so verfahren wird, ist deine
Entscheidung** — solange kein Remote existiert, ist die Frage nicht dringend,
aber sie gehört vor dem ersten Build beantwortet.
