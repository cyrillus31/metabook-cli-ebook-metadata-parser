class NotEbookError(Exception):
    def __init__(self):
        super().__init__("Provided file is not an Ebook")

class OPFNotFoundError(Exception):
    def __init__(self):
        super().__init__(".opf file was not found")
        
class ExtNotSupportedError(Exception):
    def __init__(self, extension):
        super().__init__(f"Extension {extension} is not yet supported")

class UnexpectedXMLStructureError(Exception):
    def __init__(self):
        super().__init__(f"Internal structure of the XML file is unexpected")
