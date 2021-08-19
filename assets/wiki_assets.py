import wikipedia


def wiki_search(search_term: str, limit: int = 5, suggest: bool = False):
    results = wikipedia.search(search_term, results=limit, suggestion=suggest)
    return results


def wiki_result(search_term: str):
    search_results = wiki_search(search_term, suggest=True)
    wiki_page = wikipedia.page(search_results[0][0])
    name = wiki_page.title
    summary = wiki_page.summary
    url = wiki_page.url
    images = wiki_page.images
    links = wiki_page.links
    print(wiki_page.categories)
    if len(links) > 5:
        links = links[:5]
    suggestion = [search_results[1] if search_results[1] else None]
    return name, summary, suggestion[0], url, images, links

