from dotenv import load_dotenv
import os

load_dotenv()

DEVELOPER_KEY = os.getenv("DEVELOPER_KEY")

if DEVELOPER_KEY is None:
    raise ValueError("No API key found. Please set the DEVELOPER_KEY environment variable.")
