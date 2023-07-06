# Package to parse VNExpress news
from typing import Union
import requests
from bs4 import BeautifulSoup
import model
import utils


def fetch_vne_category(url: str) -> [model.NewsTitleSummary]:
    result = []
    html = requests.get(url).content
    soup = BeautifulSoup(html, features="html.parser")
    article_nodes = soup.select('article')
    for anode in article_nodes:
        title = anode.select_one('h3.title-news > a')
        summary = anode.select_one('p.description')
        location = anode.select_one('p.description > a > span.location-stamp')
        if title is not None and summary is not None:
            url = title['href'].strip()
            title = title.text.strip()
            summary = summary.text.strip()
            if location is not None:
                summary = summary[len(location.text.strip()):]
            result.append(model.NewsTitleSummary(
                hash=utils.md5(title)+"."+utils.sha1(title),
                repo="VNExpress",
                url=url,
                title=title,
                summary=summary,
                embeddings=[],
            ))
    return result


def fetch_vne_article(item: model.BaseItem) -> Union[model.NewsTitleSummaryContent,None]:
    html = requests.get(item.url).content
    soup = BeautifulSoup(html, features="html.parser")
    title = soup.select_one('h1.title-detail')
    summary = soup.select_one('p.description')
    location = soup.select_one('p.description > span.location-stamp')
    p_nodes = soup.select('article > p')
    if title is not None and summary is not None and len(p_nodes) > 0:
        title = title.text.strip()
        summary = summary.text.strip()
        if location is not None:
            summary = summary[len(location.text.strip()):]
        paragraphs = []
        for pnode in p_nodes[:3]:
            paragraphs.append(pnode.text.strip())
        return model.NewsTitleSummaryContent(
            id=item.id,
            hash=item.hash,
            repo=item.repo,
            url=item.url,
            embeddings=item.embeddings,
            embedding_model=item.embedding_model,
            title=title,
            summary=summary,
            paragraphs=paragraphs,
        )
    return None
