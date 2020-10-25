class Review:
    """A class to store individual review
    objects.
    """
    def __init__(self, title, body, rating, *args, **kwargs):
        self.title = title
        self.body = body
        self.rating = rating
        
    def __str__(self):
        return f'Review: title: {self.title}, body: {self.body}, rating: {self.rating}'
    
    def __repr__(self):
        return f'Review Object:(title: {self.title}, body: {self.body}, rating: {self.rating})'