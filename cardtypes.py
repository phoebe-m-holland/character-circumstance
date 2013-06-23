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


CardTypes = { "Object" : Object }

