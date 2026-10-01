from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
from rich import print
import os
from dotenv import load_dotenv
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query : str) -> str:
    """Search the web for recent and reliable information on topic. Returns Titles, URLs and Snippets. """
    try:
        results = tavily.search(query=query, max_results=3)

        return "\n\n".join(
            f"{i}. {r['title']}\n"
            f"   URL: {r['url']}\n"
            f"   Summary: {r['content']}"
            for i, r in enumerate(results["results"], 1)
        )

    except Exception as e:
        return f"Search error: {e}"




@tool
def scrape_url(url: str) -> str:
    """Scrape URL and return clean text, max 1500 words."""
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        r.raise_for_status()
        s = BeautifulSoup(r.text, "lxml")

        for x in s(["script", "style", "nav", "footer", "header"]):
            x.decompose()

        text = " ".join(s.get_text(" ", strip=True).split())
        return " ".join(text.split()[:1500])

    except Exception as e:
        return f"Could not scrape url: {str(e)}"
    
