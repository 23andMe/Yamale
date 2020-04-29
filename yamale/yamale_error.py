class YamaleError(ValueError):
    def __init__(self, results):
        super(YamaleError, self).__init__('\n'.join([str(x) for x in results]))
        self.message = self.args[0]
        self.results = results
