from html2image import Html2Image
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()
STATIC_DIR = Path(os.getenv("PROJECT_SRC"), "static")

def screenshot_html(html_content, output_path="current_image.png"):
    hti = Html2Image()
    hti.output_path =  STATIC_DIR.resolve()
    hti.screenshot(html_str=html_content, save_as=output_path)