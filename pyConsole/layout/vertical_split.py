from ..utils import call

from .split import SplitScreen


class VerticalSplitScreen(SplitScreen):

    def __init__(self, **kwargs):
        super(VerticalSplitScreen, self).__init__(**kwargs)
        self.top_height = self.a.height if self.a.height > 0 else None
        self.bottom_height = self.b.height if self.b.height > 0 else None

    def onResize(self, x, y, w, h):
        self.width = w
        self.height = h
        self.x = x
        self.y = y

        if self.top_height and self.bottom_height:
            top_half = self.top_height
            bottom_half = self.bottom_height
        elif self.top_height:
            if self.top_height < h:
                top_half = self.top_height
            else:
                top_half = h + 1
            bottom_half = h - top_half
        elif self.bottom_height:
            bottom_half = self.bottom_height
            top_half = h - bottom_half
        else:
            top_half = int(round(h / 2, 0))
            bottom_half = h - top_half

        self.top_half = top_half
        self.bottom_half = bottom_half

        call(self.a, 'onResize', x, y, w, self.top_half)
        call(self.b, 'onResize', x, y + self.top_half, w, self.bottom_half)

    def render(self):
        out = []

        index = self.y

        a = call(self.a, 'render') or []
        b = call(self.b, 'render') or []

        for item in a:
            index += 1
            out.append(u'\033[{1};{0}H{2}'.format(self.x, index, item))  # noqa

        index = self.y

        for item in b:
            index += 1
            out.append(u'\033[{1};{0}H{2}'.format(self.x, index + self.top_half, item))  # noqa

        return out
