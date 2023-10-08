from dataclasses import dataclass

@dataclass
class BookMetaData:
    title: str | None = None
    author: str | None = None
    publisher: str | None = None
    date_published: str | None = None
    description: str | None = None
    language: str | None = None

    verbose: bool = False

    def __str__(self):
        if not self.verbose:
            return f"""
Title: {self.title}
Author: {self.author}
Publisher: {self.publisher}
Date published: {self.date_published}"""

        return f"""
Title: {self.title}
Author: {self.author}
Publisher: {self.publisher}
Date published: {self.date_published}
Language: {self.language}
Description: {self.description}
"""
