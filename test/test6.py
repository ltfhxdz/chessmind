import math


def mianji(box1, bofinal):
    # 方1
    x1, y1, final, y2 = box1
    print(x1, y1, final, y2)
    x1, final = min(x1, final), max(x1, final)
    y1, y2 = min(y1, y2), max(y1, y2)
    print(x1, y1, final, y2)

    # print(x1, y1, final, y2)

    # 方2
    x3, y3, x4, y4 = bofinal
    print(x3, y3, x4, y4)
    x3, x4 = min(x3, x4), max(x3, x4)
    y3, y4 = min(y3, y4), max(y3, y4)
    print(x3, y3, x4, y4)

    if (final <= x3 or x4 <= x1) and (y2 <= y3 or y4 <= y1):
        print(0)
    else:
        lens = min(final, x4) - max(x1, x3)
        wide = min(y2, y4) - max(y1, y3)
        print(lens)
        print(wide)
        print(lens * wide)


box1 = (100, 18, 300, 300)
bofinal = (200, 60, 100, 100)
mianji(box1, bofinal)
