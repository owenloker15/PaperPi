from html2image import Html2Image
from dotenv import load_dotenv
import os
from pathlib import Path
from PIL import Image

try:
    from inky.auto import auto
    inky = auto()
    IS_PI = True
except (ImportError, RuntimeError):
    inky = None
    IS_PI = False

load_dotenv()
STATIC_DIR = Path(os.getenv("PROJECT_SRC"), "static")

def screenshot_html(html_content, output_filename="current_image.png"):
    hti = Html2Image(
    custom_flags=[
        "--headless",
        "--no-sandbox",
        "--disable-gpu",
        "--disable-software-rasterizer",
        "--disable-dev-shm-usage",
        "--disable-extensions",
        "--disable-features=TranslateUI,Notifications",
        "--no-first-run",
        "--no-default-browser-check",
    ]
)
    hti.output_path = STATIC_DIR.resolve()
    hti.screenshot(html_str=html_content, save_as=output_filename)

def send_to_pi():
    img_path = STATIC_DIR / "current_image.png"
    
    img = Image.open(img_path)
    
    if IS_PI and inky is not None:
        img = img.resize(inky.resolution)
        inky.set_image(img)
        inky.show()
    else:
        img.show()  # open on Windows for preview/debug
        print("No Inky hardware detected.")
