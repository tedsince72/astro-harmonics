# Running the tools on Eddie's Mac (9 Oct 2026)

The repo stays the master copy. On the Mac there are three folders:

| folder | what it is |
|---|---|
| `~/astro-harmonics` | the clone of this repo — scripts, data, docs. Edit scripts here. |
| `~/astro-work` | the working folder the tools run in (made by `setup.sh`; the scripts' `/home/claude` paths are rewritten to it) |
| `~/astro-venv` | the Python environment (3.12 or newer) |

`~/astronomy-project` (the race cards and workbooks) is not needed for the 96 races already in the repo (`data/allpos`); it is only needed
when a new race has to be exported.

## One-time setup (Terminal)
1. Python 3.12 or newer. Check with `python3 --version`. If it is older, install Python 3.12 from python.org (the macOS installer), then open a
   new Terminal window. With Homebrew instead: `brew install python@3.12`.
2. Git: `git --version` (if macOS offers to install the command line tools, accept).
3. Get the repo (it is private, so GitHub has to know it is you — GitHub Desktop, or `brew install gh` then `gh auth login`):
   ```
   cd ~
   git clone https://github.com/tedsince72/astro-harmonics.git
   ```
4. The Python environment:
   ```
   python3.12 -m venv ~/astro-venv
   source ~/astro-venv/bin/activate
   ```
5. The working folder:
   ```
   cd ~/astro-harmonics
   ASTRO_HOME=~/astro-work bash setup.sh
   ```
   It ends with `working folder ready: /Users/<you>/astro-work`. It fails loudly if anything is missing.

## The check — rebuild Doncaster and compare (about 25 minutes, less on a fast Mac)
```
source ~/astro-venv/bin/activate
mkdir -p ~/astro-work/rr/20220318_doncaster_1440/notes
cp ~/astro-harmonics/rr/20220318_doncaster_1440/notes/*.md ~/astro-work/rr/20220318_doncaster_1440/notes/
cd ~/astro-work
python3 tools/runner_record.py 20220318_doncaster_1440 --jobs 4
diff -rq -x '*.json' ~/astro-harmonics/rr/20220318_doncaster_1440/records ~/astro-work/rr/20220318_doncaster_1440/records && echo "SAME - the Mac reproduces the .md records"
```
All 15 `.md` records must be identical. The `.json` records may differ only in the last digits of numbers: compare numeric values to a tolerance of 1e-12; everything else must match exactly. (Tested in a cloud session on 9 Oct with a working folder other than /home/claude: identical. Mac, 9 Oct 2026: .md identical; 5 .json files differed at ~1e-16 in `natal_dev`/`sky_dev`, accepted.)

The Mac is now the reference machine: races are built here. A race is never built in two places.

## Every session after that
- Start: `source ~/astro-venv/bin/activate`, then `cd ~/astro-harmonics && git pull`.
- A script changed in the repo → run `ASTRO_HOME=~/astro-work bash setup.sh` again (scripts are refreshed, data is kept).
- Run the tools in `~/astro-work` (e.g. `python3 tools/runner_record.py <RACE>`; `python3 tools/race_table.py <RACE>`).
- Results go back into the repo: copy `~/astro-work/rr/<RACE>/records`, `notes` and `compare` into `~/astro-harmonics/rr/<RACE>/`, commit,
  `git pull`, `git push`. Summaries and walk-throughs to the project as before.
- A new race needs its off time and duration in `reference/races.csv` (then `setup.sh` again).
