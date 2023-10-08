from abc import ABC, abstractmethod

from ebook.metadata_dataclass import BookMetaData

class Ebook(ABC):
    @abstractmethod
    def get_metadata(self) -> BookMetaData:
        raise NotImplementedError

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        raise NotImplementedError
