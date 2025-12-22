import os
from dotenv import load_dotenv
import dagshub

# Load local .env only for local testing
load_dotenv()

# Print environment variable (for debugging)
print("DAGSHUB_TOKEN:", os.getenv("DAGSHUB_TOKEN"))

# Check if token exists
if not os.getenv("DAGSHUB_TOKEN"):
    print("❌ DAGSHUB_TOKEN not found. Check Render environment variables.")
else:
    print("✅ DAGSHUB_TOKEN found. Trying to initialize DagsHub...")

    try:
        dagshub.init(
            repo_owner="jaivenkateshofficial-lgtm",
            repo_name="cybersecurity",
            mlflow=True
        )
        print("✅ DagsHub initialized successfully!")
    except Exception as e:
        print("❌ DagsHub authentication failed:", e)
