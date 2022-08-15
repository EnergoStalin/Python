class DownloaderBase:
    LINK_REGEX = ""
    def __init__(self, args):
        pass
    @classmethod
    def AddArguments(cls, parser):
        pass
    def Download(self, data):
        pass