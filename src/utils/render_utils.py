from PIL import Image
from flask import current_app

from playwright.sync_api import sync_playwright
from io import BytesIO

def screenshot_html(html_content):
    width, height = current_app.config["Display_Manager"].get_resolution()
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height})
        page.set_content(html_content)
        png_bytes = page.screenshot()
        browser.close()
        # Load into PIL
        img = Image.open(BytesIO(png_bytes))
        return img
