class Place(object):
    def __init__(self, id, name, type, url, image, summary):
        self.id = id
        self.name = name
        self.type = type
        self.url = url
        self.image = image
        self.summary = summary





    def __str__(self) -> str:
        return f"{self.id}|{self.name}|{self.type}"