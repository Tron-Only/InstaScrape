import csv
import json
import time
from pathlib import Path
from urllib.parse import quote

from playwright.sync_api import sync_playwright


def _write_txt(path: Path, data: list[dict]) -> None:
    """Write results in human-readable block format."""
    lines = []
    for row in data:
        lines.append(f"Account Link: {row['Account Link']}")
        lines.append(f"Account Name: {row['Account Name']}")
        lines.append("-" * 40)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_csv(path: Path, data: list[dict]) -> None:
    """Write results as CSV with columns: #, Account Name, Account Link."""
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["#", "Account Name", "Account Link"])
        for row in data:
            writer.writerow(
                [row["Account Number"], row["Account Name"], row["Account Link"]]
            )


def _write_json(path: Path, data: list[dict]) -> None:
    """Write results as pretty JSON."""
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


_WRITERS = {
    "txt": _write_txt,
    "csv": _write_csv,
    "json": _write_json,
}


def build_query(niche: str, match_all=True) -> str:
    site_params = 'site:instagram.com -inurl:"/p" -inurl:"/reel" -inurl:"/reels" -inurl:"/explore"'
    keywords = niche.split()
    if match_all:
        joined = " ".join(f'"{kw}"' for kw in keywords)
    else:
        joined = " OR ".join(f'"{kw}"' for kw in keywords)
    return quote(f"{joined} {site_params}")


def scrape_instagram_accounts(
    niche: str,
    max_pages: int = 3,
    headless: bool = False,
    output_path: str = "results.json",
    format: str = "json",  # <- new parameter
):
    if format not in _WRITERS:
        raise ValueError(f"Unsupported format: {format}. Choose from {list(_WRITERS)}")

    query = build_query(niche, match_all=True)
    results_data = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=headless)
        page = browser.new_page()
        page.goto(f"https://www.startpage.com/search?q={query}", timeout=0)
        time.sleep(2)

        results = page.locator(".result")
        account_number = 1
        current_page = 1

        while current_page <= max_pages:
            for i in range(results.count()):
                result = results.nth(i)
                account_link = result.locator(".default-link-text").inner_text()
                account_name = result.locator(".wgl-title").inner_text().strip()
                if account_name.startswith("("):
                    try:
                        account_name = account_name[
                            : account_name.index(")") + 1
                        ].strip()
                    except ValueError:
                        pass
                else:
                    account_name = account_name.split("(")[0].strip()
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
                time.sleep(3)
                current_page += 1
            else:
                break

        browser.close()

    # choose writer and correct extension
    path = Path(output_path).with_suffix(f".{format}")
    _WRITERS[format](path, results_data)
