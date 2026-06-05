import os
import json
import requests
from google import genai
def get_pr_diff_and_urls():
    """Reads the cloud data file provided by GitHub Actions and extracts the PR diff and URLs."""
    #GitHub automatically tells us where the data file is located via the GITHUB_EVENT_PATH environment variable.
    event_path = os.getenv('GITHUB_EVENT_PATH')
    if not event_path:
        raise FileNotFoundError("GITHUB_EVENT_PATH environment variable is not set.")
    #Open and read the giant text file full of PR data
    with open(event_path, 'r') as f:
        event_data = json.load(f)
    #Extract the exact link showing what code chnanged
    diff_url = event_data.get["pull_request"]["comments_url"]
    #use the 'request' library to downlaod the raw code text change across the internet
    #GitHub automatically provides a temporary token for us to use in the header to authenticate our request
    headers = {
        'Authorization': f'token {os.getenv("GITHUB_TOKEN")}'
    }
    response = requests.get(diff_url, headers=headers)
    response.raise_for_status()  # Check if the request was successful
    return response.text, comments_url
def analyze_code_with_gemini(diff_text):
    """Uses the Gemini API to analyze the code diff and generate a review."""
    #Initialize the Gemini API client
    client = genai.Client()
    system_instruction =(
        "You are an expert Senior Software Engineer with 20 years of experience in code review. You have a deep understanding of software design principles, best practices, and common pitfalls. Your task is to analyze the provided code diff and generate a comprehensive code review that includes: \n"
        "1. A summary of the changes made in the code diff.\n"
        "2. An assessment of the code quality, including readability, maintainability, and adherence to best practices.\n"
        "3. Identification of any potential bugs, security vulnerabilities, or performance issues introduced by the changes.\n"
        "4. Suggestions for improvement, including specific recommendations for refactoring, optimization, or enhancement of the code.\n"
    )
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f"Please review this git diff:\n\n{diff_text}",
        config={
            "system_instruction": system_instruction,
            "temperature": 0.2,
        }
    )
    return response.text
def post_github_comment(review_text, comments_url):
    """Posts the generated review as a comment on the GitHub PR."""
    headers = {
        'Authorization': f'token {os.getenv("GITHUB_TOKEN")}',
        "Accept": "application/vnd.github.v3+json"
    }
    # Package our message into a neat JSON envelope to send to GitHub
    payload={"body":f"### AI Code Reviewer Feedback:\n\n{review_text}"}
    #Send it back to GitHub's servers
    response = requests.post(comments_url, headers=headers, json=payload)
    response.raise_for_status()  # Check if the request was successful
if __name__ == "__main__":
    try:
        print("Fetching code changes from Pull Request...")
        diff_text, comments_url = get_pr_diff_and_urls()
        print("Analyzing code changes with Gemini API...")
        review_text = analyze_code_with_gemini(diff_text)
        print("Posting review back to GitHub...")
        post_github_comment(review_text, comments_url)
        print("Code review posted successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
        
        