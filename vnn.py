# Package to parse VietnamNet news
from typing import Union
import requests
from bs4 import BeautifulSoup
import model
import utils


def fetch_vnn_category(url: str) -> [model.NewsTitleSummary]:
    result = []
    html = requests.get(url).content
    soup = BeautifulSoup(html, features="html.parser")
    article_nodes = soup.select('div.horizontalPost__main')
    for anode in article_nodes:
        title = anode.select_one('h3.vnn-title > a')
        summary = anode.select_one('div.horizontalPost__main-desc > p')
        if title is not None and summary is not None:
            url = title['href'].strip()
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://vietnamnet.vn"+url
            title = title.text.strip()
            summary = summary.text.strip()
            result.append(model.NewsTitleSummary(
                hash=utils.md5(title)+"."+utils.sha1(title),
                repo="VietnamNet",
                url=url,
                title=title,
                summary=summary,
                embeddings=[],
            ))
    return result


def fetch_vnn_article(item: model.BaseItem) -> Union[model.NewsTitleSummaryContent,None]:
    html = requests.get(item.url).content
    soup = BeautifulSoup(html, features="html.parser")
    title = soup.select_one('h1.content-detail-title')
    summary = soup.select_one('h2.content-detail-sapo')
    p_nodes = soup.select('div.maincontent > p')
    if title is not None and summary is not None and len(p_nodes) > 0:
        title = title.text.strip()
        summary = summary.text.strip()
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
