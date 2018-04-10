import re


def get_title_from_head(doc):
    node = doc.title
    if node:
        title = node.text
        for splitter in TITLE_SPLITTERS:
            parts = splitter.split(title)

            if len(parts) > 1:
                title = max(parts, key=len)
        return title


TITLE_SPLITTERS = (
    re.compile(r' \| '),
    re.compile(r' - '),
    re.compile(r' : '),
)


def get_title_from_h1(doc):
    nodes = list(doc.find_all('h1'))
    if len(nodes) == 1:
        return nodes[0].text


def score_title(title):
    length = len(title)
    if length > 150 or length < 15:
        return -1
    return length


def get_title(doc):
    candidates = []
    for get_title_func in TITLE_GETTERS:
        title = get_title_func(doc)
        if title:
            title_score = score_title(title)
            candidates.append((title, title_score))

    return max(candidates, key=lambda candidate: candidate[1])[0]


TITLE_GETTERS = (
    get_title_from_head,
    get_title_from_h1,
)
