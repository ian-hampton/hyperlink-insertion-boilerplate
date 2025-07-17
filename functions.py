import sqlite3

def create_links_dict(own_article_name: str):

    links = {}

    conn = sqlite3.connect("birds.db")
    curr = conn.cursor()

    curr.execute("SELECT article_name FROM articles;")
    results = curr.fetchall()
    
    # create article name -> hyperlink pairs
    for row in results:
        article_name = row[0]
        url = article_name.strip().lower().replace(" ", "_")
        links[article_name] = f"""<a href="{url}">{article_name}</a>"""

    # delete reference to own page
    del links[own_article_name]

    return links

def insert_links(article_data: dict, links: dict):
    
    nested_search(article_data["articleContent"], links)

def nested_search(content: any, links):
    
    if isinstance(content, dict):
        for key, value in content.items():
            if isinstance(value, str) and "filepath" not in key.lower():
                content[key] = insert_links_into_string(value, links)
            elif isinstance(value, (list, dict)):
                content[key] = nested_search(value, links)

    elif isinstance(content, list):
        for i, value in enumerate(content):
            if isinstance(value, str):
                content[i] = insert_links_into_string(value, links)
            elif isinstance(value, (list, dict)):
                content[i] = nested_search(value, links)

    elif isinstance(content, str):
        content = insert_links_into_string(value, links)
    
    return content

def insert_links_into_string(value: str, links: dict):

    matches = []

    # insert all possible hyperlinks to articles, but only first occurrence
    for article_name, hyperlink_str in links.items():
        index = value.find(article_name)
        if index != -1 and not value[index-1].isalnum() and not value[index+len(article_name)].isalnum():
            value = value.replace(article_name, hyperlink_str, 1)
            matches.append(article_name)
    
    # delete entry so that hyperlinks are not inserted elsewhere on page
    for article_name in matches:
        del links[article_name]

    return value
