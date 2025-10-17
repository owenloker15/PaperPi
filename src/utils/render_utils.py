from dotenv import load_dotenv
import os
from pathlib import Path
from PIL import Image
import subprocess
import tempfile

try:
    from inky.auto import auto
    inky = auto()
    IS_PI = True
    print("Inky found!")
except (ImportError, RuntimeError):
    inky = None
    IS_PI = False
    print("Inky NOT found!")

load_dotenv()
STATIC_DIR = Path(os.getenv("PROJECT_SRC"), "static")

def screenshot_html(html_content):
    output_image = None
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as img_file:
        img_file_path = img_file.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_html:
        tmp_html.write(html_content.encode("utf-8"))
        tmp_html_path = tmp_html.name

    command = [
        "chromium-headless-shell",
        tmp_html_path,
        "--headless",
        f"--screenshot={img_file_path}",
        f"--window-size={800},{480}",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--use-gl=swiftshader",
        "--hide-scrollbars",
        "--in-process-gpu",
        "--js-flags=--jitless",
        "--disable-zero-copy",
        "--disable-gpu-memory-buffer-compositor-resources",
        "--disable-extensions",
        "--disable-plugins",
        "--mute-audio",
        "--no-sandbox"
    ]

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Check if the process failed or the output file is missing
        if result.returncode != 0 or not os.path.exists(img_file_path):
            print("Failed to take screenshot:")
            print(result.stderr.decode('utf-8'))
            return None

        # Load the image using PIL
        with Image.open(img_file_path) as img:
            output_image = img.copy()

        # Remove image files
        os.remove(img_file_path)

    except Exception as e:
        print(f"Failed to take screenshot: {str(e)}")

    return output_image

def send_to_pi(img: Image):
    if img is None:
        print("No image found!")
        return

    print(inky.__class__.__name__)

    if IS_PI and inky is not None:
        print(img.mode, inky.resolution)
        print("Uploading to ink display!")

        # 🔧 Force proper image mode and memory layout
        img = img.convert("RGB").resize(inky.resolution)
        img.load()  # ensure data is loaded into memory, not lazy

        print("after resize")
        inky.set_image(img)
        print("before show")
        inky.show()
        print("Uploaded to ink display!")
    else:
        img.show()
        print("No Inky hardware detected.")

