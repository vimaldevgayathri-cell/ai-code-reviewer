# Automated AI Code Reviewer

A GitHub Actions bot that reviews your Pull Requests with Google Gemini.

Whenever a Pull Request (PR) into `main` is opened or updated, the bot reads the code changes, asks Gemini to review them like a senior engineer, and posts the review as a comment on the PR.

---

## How it works

1. **Trigger:** a PR into `main` is opened, or new commits are pushed to it.
2. **Environment:** GitHub Actions starts a temporary Ubuntu machine and installs Python and the dependencies.
3. **Fetch:** `review.py` downloads the PR's code changes (the diff) using the GitHub API.
4. **Review:** the diff is sent to Gemini with instructions to act as a senior software engineer.
5. **Comment:** the review is posted on the PR under the heading **AI Code Reviewer Feedback**.

## Files in this repo

| File | What it is |
|---|---|
| `review.py` | The reviewer. Runs **only inside GitHub Actions** (it needs data GitHub provides). |
| `.github/workflows/reviewer-pipeline.yml` | Tells GitHub when and how to run `review.py`. |
| `test_local.py` | Lets you try the Gemini part on your own PC. Nothing is posted to GitHub. |
| `brokencode.py` | A deliberately buggy example file. Edit it in a PR to see the bot find bugs. |
| `requirements.txt` | Python packages needed (`google-genai`, `requests`). |

---

## Setup (about 5 minutes)

**You need:** a GitHub account, a repository you own (create one or fork this one), and a Google AI Studio API key.

### 1. Get a Gemini API key
Create one at <https://aistudio.google.com/apikey> and copy it.

### 2. Add the key to your repository as a secret
1. Open your repo on GitHub, then **Settings → Secrets and variables → Actions**.
2. Click **New repository secret**.
3. Name: `GOOGLE_API_KEY` (exactly this, capital letters)
4. Value: paste your key, then click **Add secret**.

> Secrets are stored per repository. If you fork this repo, add the secret to your fork too. Never write your key into the code.

### 3. Check that Actions is enabled
Open the **Actions** tab. If GitHub shows a green button asking you to enable workflows (this happens on forks), click it.

### 4. Try it
1. Create a branch and change any file (for example, add a function to `brokencode.py`).
2. Push the branch and open a Pull Request **into `main`**.
3. Open the **Actions** tab and click the running workflow to watch it.
4. After about a minute, the review appears as a comment on the PR.

---

## Testing on your own PC

`review.py` cannot run locally, because GitHub supplies the PR data. To test the Gemini part instead:

**Windows (PowerShell)**
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
$env:GOOGLE_API_KEY = "your-key-here"
python test_local.py
```

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export GOOGLE_API_KEY="your-key-here"
python test_local.py
```

`test_local.py` reviews your uncommitted changes. To review everything that differs from `main`, run `python test_local.py main`. For a brand-new file, run `git add -N filename` first so git can see it.

The key only lasts for the terminal window where you set it.

---

## Troubleshooting

| What you see | Cause and fix |
|---|---|
| `GOOGLE_API_KEY is missing or empty` | The secret is missing or misspelled. Redo step 2. |
| `403 Resource not accessible by integration` | The PR comes from a fork. GitHub hides secrets from fork PRs. Use a branch in the same repo. |
| `404 ... model is no longer available` | Google retired the model. Set the `GEMINI_MODEL` environment variable, or change the default at the top of `review.py`. |
| `503 ... high demand` | Google is busy. The script retries automatically up to 5 times. If it still fails, re-run the job later. |
| No workflow run appears | The PR must target `main`, and the workflow file must be in `.github/workflows/`. Check the YAML for typos. |
| Script prints nothing locally | Save your files in your editor (Ctrl+S) before running. |

## Limitations

- PRs opened from forks don't get secrets, so the bot can't review them.
- Every new push to a PR adds a **new** comment instead of updating the old one.
- Very large diffs are cut to 100,000 characters before review.
- AI reviews can be wrong or padded. Treat them as a second opinion, not a verdict.

## Tech stack

- Python 3.10+
- Google GenAI SDK (`google-genai`), default model `gemini-3.6-flash` (override with `GEMINI_MODEL`)
- GitHub Actions
- `requests` for the GitHub API