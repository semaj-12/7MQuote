import os
import base64
import logging
import requests
import tkinter as tk
from tkinter import filedialog, messagebox
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Autodesk Forge credentials
FORGE_CLIENT_ID = os.getenv("FORGE_CLIENT_ID")
FORGE_CLIENT_SECRET = os.getenv("FORGE_CLIENT_SECRET")
FORGE_BASE_URL = "https://developer.api.autodesk.com"

# Global variable for the selected file
selected_file_path = None


def authenticate_forge():
    """Authenticate with Autodesk Forge and return token data."""
    try:
        url = f"{FORGE_BASE_URL}/authentication/v2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "client_id": FORGE_CLIENT_ID,
            "client_secret": FORGE_CLIENT_SECRET,
            "grant_type": "client_credentials",
            "scope": "data:read data:write data:create bucket:create"
        }
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        token_data = response.json()
        logger.info("Successfully authenticated with Forge.")
        return token_data
    except Exception as e:
        logger.error(f"Error authenticating with Forge: {e}")
        messagebox.showerror("Error", f"Authentication failed: {e}")
        return None


def upload_file_to_forge():
    """Upload a file to Autodesk Forge."""
    global selected_file_path
    if not selected_file_path:
        messagebox.showwarning("No File", "Please select a file first!")
        return

    try:
        token_data = authenticate_forge()
        if not token_data:
            return

        access_token = token_data.get("access_token")
        if not access_token:
            raise Exception("Access token missing.")

        bucket_key = "your_bucket_key"  # Replace with your actual Forge bucket key
        file_name = os.path.basename(selected_file_path)
        url = f"{FORGE_BASE_URL}/oss/v2/buckets/{bucket_key}/objects/{file_name}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/octet-stream"
        }

        with open(selected_file_path, "rb") as file:
            response = requests.put(url, headers=headers, data=file)
            response.raise_for_status()

        result = response.json()
        urn = result.get("objectId")
        messagebox.showinfo("Success", f"File uploaded successfully! URN: {urn}")
        logger.info("File uploaded successfully.")

        return urn
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        messagebox.showerror("Error", f"Upload failed: {e}")
        return None


def translate_file():
    """Trigger translation of the uploaded file."""
    urn = upload_file_to_forge()
    if not urn:
        return

    try:
        token_data = authenticate_forge()
        if not token_data:
            return

        access_token = token_data.get("access_token")
        if not access_token:
            raise Exception("Access token missing.")

        url = f"{FORGE_BASE_URL}/modelderivative/v2/designdata/job"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "input": {"urn": base64.b64encode(urn.encode()).decode()},
            "output": {"formats": [{"type": "svf", "views": ["2d", "3d"]}]}
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        translation_result = response.json()
        messagebox.showinfo("Success", "Translation initiated successfully!")
        logger.info("Translation initiated successfully.")

        return translation_result
    except Exception as e:
        logger.error(f"Error translating file: {e}")
        messagebox.showerror("Error", f"Translation failed: {e}")
        return None


def select_file():
    """Open file dialog to select a file."""
    global selected_file_path
    selected_file_path = filedialog.askopenfilename(title="Select a file")
    if selected_file_path:
        file_label.config(text=f"Selected: {os.path.basename(selected_file_path)}")
    else:
        file_label.config(text="No file selected")


# Create Tkinter GUI
root = tk.Tk()
root.title("Forge File Uploader")

# Window size
root.geometry("400x250")

# Select file button
file_label = tk.Label(root, text="No file selected", wraplength=300)
file_label.pack(pady=5)

select_button = tk.Button(root, text="Select File", command=select_file)
select_button.pack(pady=5)

# Upload file button
upload_button = tk.Button(root, text="Upload File", command=upload_file_to_forge)
upload_button.pack(pady=5)

# Translate file button
translate_button = tk.Button(root, text="Translate File", command=translate_file)
translate_button.pack(pady=5)

# Run the Tkinter app
root.mainloop()
