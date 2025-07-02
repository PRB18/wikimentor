import streamlit as st
import requests

# 📘 Wikipedia summary
@st.cache_data(show_spinner=False)
def fetch_topic_summary(topic):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("extract", "No summary available.")
    return None

# 📚 Wikibooks search
@st.cache_data(show_spinner=False)
def fetch_wikibooks_links(topic):
    api_url = "https://en.wikibooks.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": topic,
        "format": "json"
    }
    response = requests.get(api_url, params=params)
    books = []
    if response.status_code == 200:
        for result in response.json().get("query", {}).get("search", []):
            title = result["title"]
            url = f"https://en.wikibooks.org/wiki/{title.replace(' ', '_')}"
            books.append((title, url))
    return books

# 🧠 Wikidata facts (entity-based)
@st.cache_data(show_spinner=False)
def fetch_wikidata_facts(topic):
    search_url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbsearchentities",
        "search": topic,
        "language": "en",
        "format": "json"
    }
    search_res = requests.get(search_url, params=params)
    facts = []
    if search_res.status_code == 200 and search_res.json()["search"]:
        qid = search_res.json()["search"][0]["id"]
        entity_url = f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"
        entity_res = requests.get(entity_url)
        if entity_res.status_code == 200:
            entity_data = entity_res.json()
            claims = entity_data["entities"][qid]["claims"]
            for prop in list(claims.keys())[:5]:  # Limit to 5 facts
                try:
                    prop_label_url = f"https://www.wikidata.org/wiki/Special:EntityData/{prop}.json"
                    prop_label_res = requests.get(prop_label_url)
                    prop_label = prop_label_res.json()["entities"][prop]["labels"]["en"]["value"]

                    val_id = claims[prop][0]["mainsnak"]["datavalue"]["value"].get("id")
                    if val_id:
                        val_url = f"https://www.wikidata.org/wiki/Special:EntityData/{val_id}.json"
                        val_res = requests.get(val_url)
                        val_label = val_res.json()["entities"][val_id]["labels"]["en"]["value"]
                        facts.append(f"{prop_label}: {val_label}")
                except Exception:
                    continue
    return facts

# 🎓 Wikiversity educational resources
@st.cache_data(show_spinner=False)
def fetch_wikiversity_resources(topic):
    api_url = "https://en.wikiversity.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": topic,
        "format": "json"
    }
    response = requests.get(api_url, params=params)
    links = []
    if response.status_code == 200:
        for item in response.json().get("query", {}).get("search", []):
            title = item["title"]
            url = f"https://en.wikiversity.org/wiki/{title.replace(' ', '_')}"
            links.append((title, url))
    return links
