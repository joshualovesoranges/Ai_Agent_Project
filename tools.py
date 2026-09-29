from ddgs import DDGS
import json


def web_search(query: str) -> str:
    """
    Search the web for up to date information about the given query
    """
    print(f"Searching the web for: {query}")
    results = DDGS().text(query, max_results=5)
    formatted = []
    for r in results:
        formatted.append({
            "title": r.get("title"),
            "snippet": r.get("body")
        })
    
    return json.dumps(formatted)




