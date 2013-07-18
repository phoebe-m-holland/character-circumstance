from card import Card
from cairo import Context
from math import pi, sqrt

class Object(Card):
    def illustrate(self, surface):
        if self.art != None:
            illustration = Context(surface)
            illustration.scale(0.6, 0.6)
            illustration.translate(self.w / 6, self.h / 6)
            self.art.render_cairo(illustration)
            illustration.translate(self.w * 4 / 3, self.h * 4 / 3)
            illustration.rotate(pi)
            self.art.render_cairo(illustration)


class Talent(Card):
    def typeset(self, surface):
        self.panel(surface, self.w / 32, self.h / 16, 1, 0.5)
        # Disabled panel for now cause it's a pane
        self.panel(surface, self.h * 7 / 8, self.h * 15 / 16, 1, 0.5)
        self.renderText(surface, self.title, self.h / 16, self.w / 16, 0.2)
        self.renderText(surface, self.description, self.h * 7 / 8, self.w / 32, 0.3, w=(5,9))

    def illustrate(self, surface):
        if self.art != None:
            illustration = Context(surface)
            sf = self.w / self.art.get_dimension_data()[2]
            illustration.scale(sf, sf)
            self.art.render_cairo(illustration)
"""
    def renderText(surface, text, y_offset, size, shade, w=(3,4)):
        pass
"""
CardTypes = { "Object" : Object, "Talent" : Talent }

