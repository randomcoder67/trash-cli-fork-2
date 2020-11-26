from .assert_equals_with_unidiff import assert_equals_with_unidiff

class OutputCollector:
    def __init__(self):
        from unit_tests.myStringIO import StringIO
        self.stream = StringIO()
        self.getvalue = self.stream.getvalue
    def write(self,data):
        self.stream.write(data)
    def should_be(self, expected):
        assert_equals_with_unidiff(expected, self.output())
    def output(self):
        return self.stream.getvalue()

