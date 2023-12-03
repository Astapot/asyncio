async def to_string(string, info, session):
    seek_urls = info[string]
    seeks = []
    for url in seek_urls:
        response = await session.get(url)
        url_json = await response.json()
        name = url_json[list(url_json.keys())[0]]
        seeks.append(name)
    result = ', '.join(seeks)
    info[string] = result
    return result

