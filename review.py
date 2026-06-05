import os
from google import genai

def analyze_code_locally():
    #check if the API key is present in the environment variable(GOOGLE_API_KEY)
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY environment variable missing!.")
        return
    print("Initializing the GenAI client...")
    #the client automatically looks for the API key in the environment variable
    client = genai.Client()
    #the code to be reviewed
    # In a real-world scenario, you would read this from a file or another source
    #2. this is a mock code snippet for demonstration purposes
    mock_git_diff = """
    def calculate_area(radius):
        return 3.14159 * radius * radius
    """
    #3. create a prompt for the GenAI model
    prompt=(
        "You are a strict,helpful Senior Software Engineer. Review the provided git diff code."
        "Point out any critical logical bugs, explain why it is a bug and provide a corrected version of the code."
    )
    print("Analyzing the code for bugs...")
    #4. call the GenAI API to analyze the code
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f"Please review the following code and identify any critical logical bugs:\n\n{mock_git_diff}",
        config={
            "temperature":0.2, #keeps the ai analytical and focused on finding bugs rather than being creative
            "system_instruction":prompt
        }
    )
    print("\n--- Analysis Result ---")
    print(response.text)
if __name__ == "__main__":
    analyze_code_locally()
    

