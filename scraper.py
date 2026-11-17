
import asyncio
import json
from playwright.async_api import async_playwright

ORGANIZER_URL = "https://www.livetickets.ro/evenimente/nkt-events"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        page = await browser.new_page(
            locale="ro-RO",
            viewport={"width": 1440, "height": 1000}
        )

        print("Deschid LiveTickets...")

        await page.goto(
            ORGANIZER_URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        await page.wait_for_timeout(10000)

        events = await page.locator("a[href*='/bilete/']").evaluate_all("""
            links => links.map(a => ({
                title: a.innerText.trim(),
                url: a.href
            })).filter(e => e.url && e.title)
        """)

        unique_events = {
            event["url"]: event for event in events
        }

        events = list(unique_events.values())

        print(f"Evenimente găsite: {len(events)}")

        for event in events:
            print("-", event["title"])
            print(" ", event["url"])

        with open("events.json", "w", encoding="utf-8") as f:
            json.dump(events, f, ensure_ascii=False, indent=2)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
