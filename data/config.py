import os, ast
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("API_TOKEN")
ADMINS = ast.literal_eval(os.getenv("ADMIN_ID"))
CHANNELS = os.getenv("CHANNEL_ID")
GROUP = os.getenv("GROUP_ID")