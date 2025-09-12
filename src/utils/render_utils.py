from html2image import Html2Image

def screenshot_html(html_content, output_path="screenshot.png"):
    hti = Html2Image()
    hti.screenshot(html_str=html_content, save_as=output_path)