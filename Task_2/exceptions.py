class NotEbookError(Exception):
    def __init__(self):
        super().__init__("Provided file is not an Ebook")

class OPFNotFoundError(Exception):
    def __init__(self):
        super().__init__(".opf file was not found")
        
