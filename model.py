class BaseItem:
    def __init__(self, id: str = "", hash: str = "", repo: str = "", url: str = "", embeddings: [float] = None,
                 embedding_model: str = ""):
        self.id = id
        self.hash = hash
        self.repo = repo
        self.url = url
        self.embeddings = embeddings
        self.embedding_model = embedding_model
        from datetime import datetime
        self.timestamp = datetime.now()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "hash": self.hash,
            "repo": self.repo,
            "url": self.url,
            "embeddings": self.embeddings,
            "embedding_model": self.embedding_model,
            "timestamp": self.timestamp,
        }


class NewsTitleSummary(BaseItem):
    def __init__(self, id: str = "", hash: str = "", repo: str = "", url: str = "", embeddings: [float] = None,
                 embedding_model: str = "", title: str = "", summary: str = ""):
        super().__init__(id, hash, repo, url, embeddings, embedding_model)
        self.title = title
        self.summary = summary

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["title"] = self.title
        result["summary"] = self.summary
        return result


class NewsTitleSummaryContent(NewsTitleSummary):
    def __init__(self, id: str = "", hash: str = "", repo: str = "", url: str = "", embeddings: [float] = None,
                 embedding_model: str = "", title: str = "", summary: str = "", paragraphs: [str] = None):
        super().__init__(id, hash, repo, url, embeddings, embedding_model, title, summary)
        self.paragraphs = paragraphs

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["paragraphs"] = self.paragraphs
        return result


# ----------------------------------------------------------------------#

class BaseStorage:
    def save(self, item: BaseItem, storage: str = ""):
        pass


class ConsoleStorage(BaseStorage):
    def save(self, item: BaseItem, storage: str = ""):
        import json
        print(json.dumps(item.to_dict(), ensure_ascii=False))
