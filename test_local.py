"""Local test: sends your local git changes to Gemini and prints the review.
Nothing is posted to GitHub.

Usage (from the project folder, with GOOGLE_API_KEY set in the same terminal):
    python test_local.py         # reviews all uncommitted changes (git diff HEAD)
    python test_local.py main    # reviews everything that differs from the main branch
"""
import subprocess
import sys

from review import analyze_code_with_gemini


def get_local_diff(git_args):
    """Runs 'git diff' with the given arguments and returns the text."""
    result = subprocess.run(
        ["git", "diff", *git_args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        raise RuntimeError(f"git diff failed: {result.stderr.strip()}")
    return result.stdout


if __name__ == "__main__":
    try:
        args = sys.argv[1:] or ["HEAD"]
        diff = get_local_diff(args)

        if not diff.strip():
            print("No changes found. Edit a file first (brand-new files need: git add -N <file>).")
            sys.exit(0)

        print(f"Sending {len(diff)} characters of changes to Gemini...\n")
        print(analyze_code_with_gemini(diff))
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)