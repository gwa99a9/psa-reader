class TorrentData:
    def __init__(self, tName, tLink, tSize, tSeeds, tLeeches, tDate):
        self.tName = tName
        self.tLink = tLink
        self.tSize = tSize
        self.tSeeds = tSeeds
        self.tLeeches = tLeeches
        self.tDate = tDate

    def to_tuple(self):
        return (
            self.tName,
            self.tLink,
            self.tSize,
            self.tSeeds,
            self.tLeeches,
            self.tDate
        )
