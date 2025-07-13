import time
from urllib.parse import quote
from playwright.sync_api import sync_playwright

niche = "basketball"
site_params = f'site:instagram.com inurl:"/{niche}" intitle:"{niche}" -inurl:"/p" -inurl:"/reel" -inurl:"/explore"'
query = quote(f"{niche} {site_params}")

with sync_playwright() as pw:
    browser = pw.firefox.launch(headless=False)
    page = browser.new_page()

    # Navigate to Startpage with encoded query
    page.goto(f"https://www.startpage.com/search?q={query}", timeout=0)

    # Wait for results to load (adjust if needed)
    time.sleep(2)
    results = page.locator(".result")  # Startpage's result class

    for i in range(results.count()):
        result = results.nth(i)

        # Extract data with more specific selectors
        account_link = result.locator(".default-link-text").inner_text()
        account_name = result.locator(".wgl-title").inner_text()
        account_description = result.locator(".description").inner_text()

        print(f"Account Link: {account_link}")
        print(f"Account Name: {account_name}")
        print(f"Account Description: {account_description}")
        print("-" * 40)

    # Debugging (optional)
    page.screenshot(path="startpage_results.png")
    browser.close()
