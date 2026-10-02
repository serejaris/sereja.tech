import http.server
import socketserver
import threading
import time
import subprocess
import os

PORT = 8899
DIRECTORY = "public"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        httpd.serve_forever()

t = threading.Thread(target=start_server, daemon=True)
t.start()
time.sleep(1)

# URLs to test
url_hero = f"http://127.0.0.1:{PORT}/blog/claude-fable-5-1-v1/"
url_video = f"http://127.0.0.1:{PORT}/blog/claude-fable-5-1-v1/#video-zhir"

# Capture hero screenshot
cmd_hero = [
    "playwright", "screenshot",
    "--viewport-size=1440,1100",
    url_hero,
    "static/design-review/screenshot-v1-hero.png"
]
subprocess.run(cmd_hero, check=True)

# Capture video section screenshot
# Using playwright with python script to wait for selector and scroll
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 1100})
    page.goto(url_hero, wait_until="networkidle")
    
    # Screenshot of Pelican Hero Box specifically
    hero_elem = page.locator("#thinkingGrid")
    if hero_elem.count() > 0:
        hero_elem.screenshot(path="static/design-review/screenshot-v1-pelicans.png")
    
    # Scroll to and screenshot video-zhir section
    video_elem = page.locator("#video-zhir")
    if video_elem.count() > 0:
        video_elem.scroll_into_view_if_needed()
        time.sleep(0.5)
        video_elem.screenshot(path="static/design-review/screenshot-v1-video.png")

    # Dark mode screenshots
    page.locator("#themeBtn").click()
    time.sleep(0.3)
    if hero_elem.count() > 0:
        hero_elem.screenshot(path="static/design-review/screenshot-v1-pelicans-dark.png")
    if video_elem.count() > 0:
        video_elem.scroll_into_view_if_needed()
        time.sleep(0.5)
        video_elem.screenshot(path="static/design-review/screenshot-v1-video-dark.png")

    browser.close()

print("Captured screenshots successfully!")
