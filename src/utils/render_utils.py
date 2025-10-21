from PIL import Image
from flask import current_app
from html2image import Html2Image
import tempfile
import os

def screenshot_html(html_content):
    output_image = None
    display_manager = current_app.config["Display_Manager"]
    # resolution = display_manager.get_resolution()

    html2image = Html2Image(custom_flags=[
        "--no-sandbox",
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--disable-software-rasterizer",
        "--disable-extensions",
        "--disable-logging",
        "--headless",
        "--no-zygote",
        "--disable-dbus"])

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as img_file:
        img_file_path = img_file.name

    html2image.output_path = os.path.dirname(img_file.name)
    html2image.screenshot(html_str=html_content, save_as=os.path.basename(img_file_path))

    with Image.open(img_file_path) as img:
        output_image = img.copy()

    os.remove(img_file_path)

    return output_image
