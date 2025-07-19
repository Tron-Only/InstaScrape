import time
import json
from urllib.parse import quote
from playwright.sync_api import sync_playwright


# TODO: CHANGE headless TO TRUE
def scrape_instagram_accounts(
    niche: str,
    max_pages: int = 3,
    headless: bool = False,
    output_path: str = "results.json",
):
    site_params = 'site:instagram.com -inurl:"/p" -inurl:"/reel" -inurl:"/explore"'
    query = quote(f"{niche} {site_params}")
    results_data = []

    with sync_playwright() as pw:
        browser = pw.firefox.launch(headless=headless)
        page = browser.new_page()

        # Navigate to Startpage with encoded query
        page.goto(f"https://www.startpage.com/search?q={query}", timeout=0)

        # Wait for results to load (adjust if needed)
        time.sleep(2)
        results = page.locator(".result")  # Startpage's result class

        current_page = 1
        account_number = 1
        while current_page <= max_pages:
            for i in range(results.count()):
                result = results.nth(i)

                # Extract data with more specific selectors
                account_link = result.locator(".default-link-text").inner_text()
                account_name = (
                    result.locator(".wgl-title").inner_text().split("(")[0].strip()
                )

                results_data.append(
                    {
                        "Account Number": account_number,
                        "Account Link": account_link,
                        "Account Name": account_name,
                    }
                )
                account_number += 1

            next_button = page.locator(
                '[data-testid="pagination-button"]:has-text("Next")'
            )
            if next_button.count() > 0:
                next_button.click()
                time.sleep(3)  # Wait for next page
                current_page += 1
            else:
                print("No more pages.")
                break

        # Debugging (optional)
        page.screenshot(path="startpage_results.png")
        browser.close()

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results_data, f, indent=2, ensure_ascii=False)


scrape_instagram_accounts("Basketball", 5)
