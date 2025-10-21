from PIL import Image
from flask import current_app
from html2image import Html2Image

from playwright.sync_api import sync_playwright
from io import BytesIO

def screenshot_html(html_content, width=800, height=480):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height})
        page.set_content(html_content)
        png_bytes = page.screenshot(full_page=True)
        browser.close()
        # Load into PIL
        img = Image.open(BytesIO(png_bytes))
        return img
