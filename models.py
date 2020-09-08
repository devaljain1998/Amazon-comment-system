class Review:
    """A class to store individual review
    objects.
    """
    def __init__(self, title, body, rating, *args, **kwargs):
        self.title = title
        self.body = body
        self.rating = rating
        
    