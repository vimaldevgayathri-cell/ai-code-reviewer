# Automated AI Code Reviewer

An automated code review assistant powered by **GitHub Actions** and the **Gemini 2.5 Flash API**. 

Whenever a developer opens or updates a Pull Request, this pipeline automatically runs in the cloud to analyze the code additions, identify potential bugs or performance bottlenecks, and post constructive feedback directly into the PR conversation window.

---

## How It Works

1. **The Trigger:** A developer opens a Pull Request or pushes new changes to an existing PR.
2. **The Environment:** GitHub Actions spins up an isolated, temporary Ubuntu virtual machine in the cloud.
3. **The Script:** A Python script safely extracts the code changes (`git diff`) using the GitHub API.
4. **The Analysis:** The patch is passed to the **Gemini API** (`gemini-2.5-flash`) along with a strict system prompt instructing it to act like a Senior Software Engineer.
5. **The Feedback:** The resulting AI review report is cleanly formatted and posted automatically as a comment right on the Pull Request page.

---

##  Tech Stack

* **Language:** Python 3.10+
* **AI Engine:** Google GenAI SDK (`gemini-2.5-flash`)
* **Automation:** GitHub Actions (CI/CD workflows)
* **API Communication:** HTTP `requests` library

---

##  Setup & Installation

### 1. Repository Secret
To securely connect the pipeline to Gemini without exposing your private API key, add your key to your GitHub repository secrets:
* Go to your repository **Settings** -> **Secrets and variables** -> **Actions**.
* Click **New repository secret**.
* Name: `GOOGLE_API_KEY`
* Value: *Paste your Google AI Studio API key here*.

### 2. Local Testing
If you want to run the pipeline dependencies locally, install them using:
```bash
pip install -r requirements.txt
