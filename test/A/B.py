from test.A import D


class B:

    def __init__(self):
        print('B')

    @staticmethod
    def add():
        print('B add')


B.add()
D.Tool.add()





