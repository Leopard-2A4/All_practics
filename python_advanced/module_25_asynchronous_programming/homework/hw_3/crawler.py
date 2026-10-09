import asyncio
import aiohttp
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup

OUT_PATH = Path(__file__).parent / "links.txt"

#MAX_DEPTH = 3 #Если не хочется вводить значение глубины, раскомментируйте
MAX_DEPTH = int(input("What depth for search, do you want? "))


def extract_links(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        absolute = urljoin(base_url, href)
        links.append(absolute)
    return links


class WebCrawler:
    def __init__(self, max_depth: int = MAX_DEPTH, output_file: Path = OUT_PATH):
        self.max_depth = max_depth
        self.output_file = output_file
        self.seen_urls = set()

    async def fetch_page(self, session: aiohttp.ClientSession, url: str) -> str | None:
        """Получает HTML страницы."""
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        return None

    async def crawl(self, session: aiohttp.ClientSession, url: str, depth: int) -> None:
        """Рекурсивно обходит страницу и ссылки."""

        if depth > self.max_depth:
            return

        if url in self.seen_urls:
            return
        self.seen_urls.add(url)

        print(f"Crawling ({depth}): {url}")

        html = await self.fetch_page(session, url)
        if not html:
            return

        links = extract_links(html, url)

        with open(self.output_file, "a", encoding="utf-8") as f:
            for link in links:
                f.write(f"{link}\n")

        tasks = [
            self.crawl(session, link, depth + 1)
            for link in links
            if link not in self.seen_urls
        ]
        await asyncio.gather(*tasks)

    async def run(self, start_urls: list[str]) -> None:
        """Запуск краулера с начальных URL."""
        async with aiohttp.ClientSession() as session:
            tasks = [self.crawl(session, url, depth=1) for url in start_urls]
            await asyncio.gather(*tasks)


def main():
    OUT_PATH.unlink(missing_ok=True)

    crawler = WebCrawler(max_depth=3, output_file=OUT_PATH)
    start_urls = [
        "https://httpbin.org/links/10"
    ]

    asyncio.run(crawler.run(start_urls))

    print(f"\nВнешние ссылки записаны в {OUT_PATH}")


if __name__ == "__main__":
    main()