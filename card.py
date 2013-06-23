#!/usr/bin/env python

from cairo import Context, PDFSurface
from cairo import LINE_JOIN_ROUND as rounded
from pangocairo import CairoContext
import pango
from pango import FontDescription
from rsvg import Handle as SVG

from math import pi, sqrt
from itertools import count

class Card:
    font = "URW Palladio L, Roman"

    def __init__(self, title, description, width, height):
        self.title = title
        self.processDescription(description)
        self.w, self.h = width, height
        self.loadSVG()

    def processDescription(self, text):
        self.description = text

    def outputPDF(self):
        output = PDFSurface(None, self.w, self.h)
        self.outline(output)
        self.illustrate(output)
        self.typeset(output)
        return output

    def outline(self, surface):
        border = Context(surface)
        border.rectangle(self.w / 64, self.w / 64, self.w - self.w / 32, self.h - self.w / 32 - 2)
        border.set_line_width(self.w / 32)
        border.set_source_rgb(0.1, 0.1, 0.1)
        border.set_line_join(rounded)
        border.stroke()

    def illustrate(self, surface):
        pass

    def typeset(self, surface):
        if self.description != "":
            self.renderText(surface, self.title, self.h * 2 / 5, self.w / 16, 0)
            self.renderText(surface, self.description, self.h / 2, self.w / 32, 0.03)
        else:
            self.renderText(surface, self.title, self.h * 4 / 9, self.w / 14, 0)

    def renderText(self, surface, text, y_offset, size, shade):
        origin = Context(surface)
        origin.set_source_rgb(shade, shade, shade)
        origin.translate(self.w / 10, y_offset)
        box = CairoContext(origin)
        layout = box.create_layout()
        layout.set_font_description(FontDescription(self.font + " " + str(size)))
        layout.set_width(self.w * pango.SCALE * 5 / 6 )
        layout.set_alignment(pango.ALIGN_CENTER)
        layout.set_justify(True)
        layout.set_text(text)
        box.update_layout(layout)
        box.show_layout(layout)

    def loadSVG(self):
        svg_name = "Input/" + self.__class__.__name__ + "/" + self.title + ".svg"
        try:
            self.art = SVG(file=svg_name)
        except:
            print "Error processing", svg_name
            self.art = None

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

    def outputPDF(self, name, rows, columns):
        with open(name, 'w') as output:
            surface = PDFSurface(output, rows * self.w, columns * self.h)
            sheet = Context(surface)
            for i in count():
                if i < self.cards.__len__():
                    c, r = i % rows, (i / rows) % columns
                    sheet.set_source_surface(self.cards[i].outputPDF(), self.w * c, self.h * r)
                    sheet.rectangle(self.w * c, self.h * r, self.w, self.h)
                    if (i > 0) and not (i % (rows * columns)):
                        sheet.show_page()
                    sheet.fill()
                else:
                    break
            surface.finish()


if __name__ == "__main__":
    CardSheet(["Object"], 1024, 1536).outputPDF("Output.pdf", 3, 3)
