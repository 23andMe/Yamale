class YamaleError(ValueError):
    results: []
    def __init__(self, results):
        self.results = results
        self.message = '\n'.join([str(x) for x in results])
