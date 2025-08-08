import subprocess

def chat_with_character(prompt):
    """
    Uses Ollama with a local model like mistral or llama3.
    """
    try:
        # Run the model via subprocess and capture the output
        result = subprocess.run(
            ["ollama", "run", "mistral", prompt],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error generating dialogue: {str(e)}"
