# OrganizerTX

An AI-enabled everyday desktop for managers, engineers and project managers: research, tasks, projects, budgets, field capture, minutes and reports in one app that runs in the browser and installs on Android.

Current version: **v0.38** (see the version history at the top of `README.txt`).

## What it does

- **Research** a topic at three depths, with sources, diagrams and photos, filed as documents in project folders, with optional recurring updates.
- **My Day** briefing each morning: what is due, overdue and blocked, what changed in followed topics, and three priorities.
- **Assistant**: ask your own data, turn meeting notes into minutes and tasks, write weekly status and daily site reports, and analyse files (PDF, Word, Excel, pictures).
- **Tasks**: board, list and calendar views, owners, reminders and repeating tasks.
- **Projects**: activity plan, budget with a spend log (VAT at 0%, 16% or 18%, tied to milestones), risks and issues, milestones.
- **Data capture**: photos, voice notes, web page notes and text notes filed against a project.
- **Dashboard**, **My Desktop** file view, **AI brain** notes, editable **rules** and **skills**, colour themes, light and dark.

## Run it

1. Download or clone this repository.
2. Open `index.html` in Chrome or Edge.
3. Enter your name, country and your own Claude API key (kept on your device only).

To host it for other people, and to keep your key on a server instead of in the app, follow `README.txt`. In short: deploy `server/worker.js` as a Cloudflare Worker, put its address in `config.js`, and host these files on any static host (GitHub Pages works: Settings, Pages, deploy from the `main` branch root).

## Never commit a key

The app holds no API key. A user's key lives only in their browser; the owner's key lives only in the Worker's secret settings. Do not put a key in `config.js` or any other file here.

## What is in this repository

| Path | What it is |
|---|---|
| `index.html` | The whole app: markup, styles and script in one file |
| `sw.js`, `manifest.webmanifest`, `icon-*.png` | Offline cache and install-to-phone files |
| `config.js` | The one setting for whoever runs the app: the server address |
| `server/worker.js` | Cloudflare Worker that holds the key, checks access codes and daily limits, and sends email |
| `rules/`, `skills/` | Starter rule and skill files the app loads and lets users edit |
| `README.txt` | Full setup guide and version history |
| `build/` | Source of the starter rules and skills embedded in the app |
| `tests/` | Browser test scripts (Playwright, Python) used during development |

## Tests

The scripts in `tests/` drive the app in headless Chrome with mock AI replies. They were written for the development sandbox and expect the app served at `http://localhost:8765` (`python3 -m http.server 8765` from the repository root) and Playwright for Python installed. Some older scripts target earlier screens and will need their selectors updated.

## Status

Built and tested with mock AI replies in a test browser. Still to be confirmed on real devices: phone camera and microphone, device notifications, the folder picker, opening exports in Microsoft Word, and email sending.
