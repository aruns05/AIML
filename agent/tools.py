from langchain_community.tools.tavily_search import TavilySearchResults

def get_profile_url(name: str):
    search = TavilySearchResults()
    res= search(f"{name}")
    print('myres', res)
    return res[0]["url"]

    