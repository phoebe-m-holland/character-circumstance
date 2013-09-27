from card import Card
from cairo import Context
from math import pi, sqrt
from rsvg import Handle as SVG

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

suits = {"B": "Body", "K": "Book"}


class Talent(Card):
    def processName(self, text):
        suit, title = text.split(";")
        self.title = title.upper()
        self.name = title
        r, s = suit
        suitvg = "Input/Suits/" + suits[s] + r + ".svg"
        try:
            self.suit = SVG(file=suitvg)
        except: 
            print "Error processing icon " + suitvg
            self.suit = None

    def typeset(self, surface):
        self.renderText(surface
                , self.title, self.h / 16, self.w / 16, 0, w=(4,9), wrap=False)
        self.renderText(surface, self.description, self.h * 7 / 8, self.w / 32, 0.1, w=(4,9))

    def illustrate(self, surface):
        if self.suit != None:
            suits = Context(surface)
            suits.scale(0.5, 0.5)
            suits.translate(self.w / 8, self.h / 12)
            self.suit.render_cairo(suits)
            suits.translate(self.w * 7 / 4, self.h * 11 / 6)
            suits.rotate(pi)
            self.suit.render_cairo(suits)
        if self.art != None:
            illustration = Context(surface)
            sf = self.w / self.art.get_dimension_data()[2]
            illustration.scale(sf, sf)
            self.art.render_cairo(illustration)

CardTypes = { "Object" : Object, "Talent" : Talent }

