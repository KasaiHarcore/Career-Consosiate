import os

# Set your GROQ API key securely (avoid hardcoding in production)
# Use os.environ['Environment_API_KEY'] = "KEY" to setup
# Support: OpenAI, GROQ, OpenRouter, Claude
os.environ['OPENAI_API_KEY'] = ""
os.environ['OPENROUTER_API_KEY'] = "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"
os.environ['GROQ_API_KEY'] = ""

# Secret Key for Encrypt / Decrypt personal information
# Save this key securely and avoid hardcoding in production
SECURITY_KEY = b'12345678901234567890123456789012' # Must be 32 chars long (256 bits) - Can be anything

# Default Working Folder
default_working_folder = "./data"

# Saving failed CVs parsing
failed = []