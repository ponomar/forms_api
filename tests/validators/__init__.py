

class DummyField(object):
    def __init__(self, value, **kwargs):
        self.value = value

        for k_, v_ in kwargs.items():
            setattr(self, k_, v_)
