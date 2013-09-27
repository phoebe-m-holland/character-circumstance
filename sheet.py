#!/usr/bin/env python

from cardtypes import Card, CardTypes
from cairo import PDFSurface, Context
from itertools import count

class CardSheet:
    cards = []
    def __init__(self, cardlists, w, h):
        self.w, self.h = w, h
        for ls in cardlists:
            with open("Input/" + ls + ".list") as lines:
                for line in lines:
                    title, desc = (l.strip() for l in line.split(":"))
                    description = desc.replace(">", "\n")
                    self.cards.append(CardTypes[ls](title, description, w, h))
        self.cards.append(Card("", "", w, h))

    def outputPDF(self, name, rows, columns):
        with open(name, 'w') as output:
            surface = PDFSurface(output, rows * self.w, columns * self.h)
            sheet = Context(surface)
            for i in range(len(self.cards)):
                c, r = i % rows, (i / rows) % columns
                sheet.set_source_surface(self.cards[i].outputPDF(), self.w * c, self.h * r)
                sheet.rectangle(self.w * c, self.h * r, self.w, self.h)
                if (i > 0) and not (i % (rows * columns)):
                    sheet.show_page()
                sheet.fill()
            surface.finish()


if __name__ == "__main__":
    CardSheet(["Object", "Talent"], 1024, 1536).outputPDF("Output.pdf", 3, 3)
