#!/usr/bin/env python

import cairo
import pango
import pangocairo
import rsvg

from math import pi
from itertools import count

class Card:
    width, height = 256, 384
    font = "Sans"
    border = 4

    def __init__(self, title, description):
        im = "Input/" + self.prefix + title + ".svg"
        surface = cairo.PDFSurface(None, self.width, self.height)
        self.drawBorder(surface)
        if description != "":
            self.drawText(surface, title, self.height / 2.5, 12)
            self.drawText(surface, description, self.height / 2, 8)
        else:
            self.drawText(surface, title, self.height / 2.25, 13)
        self.drawImage(surface, self.loadSVG(im))
        self.surface = surface


    def drawBorder(self, surface):
        context = cairo.Context(surface)
        context.rectangle(self.border/2, self.border/2,
                          self.width - self.border,
                          self.height - self.border)
        context.set_line_width(self.border)
        context.set_line_join(cairo.LINE_JOIN_ROUND)
        context.stroke()

    def drawText(self, surface, text, y_offset, size):
        font = pango.FontDescription(self.font + " " + str(size))
        context = cairo.Context(surface)
        context.set_source_rgb(0, 0, 0)
        context.translate(self.width / 10, y_offset)
       
        pangocontext = pangocairo.CairoContext(context)
        layout = pangocontext.create_layout()
        layout.set_font_description(font)

        layout.set_width(self.width * pango.SCALE * 4 / 5 )
        layout.set_alignment(pango.ALIGN_CENTER)
        layout.set_text(text)
        pangocontext.update_layout(layout)
        pangocontext.show_layout(layout)

    def drawImage(self, surface, svg): 
        pass 

    def loadSVG(self, svg_name):
        try:
            return rsvg.Handle(file=svg_name)
        except:
            print "error processing " + svg_name
            return None

class Object(Card):
    prefix = "Objects/"
    def drawImage(self, surface, svg):
        if svg != None:
            context = cairo.Context(surface)
            context.scale(0.2, 0.2)
            context.translate(self.width / 2, self.height / 2)
            svg.render_cairo(context)
            context.translate(self.width * 4, self.height * 4)
            context.rotate(pi)
            svg.render_cairo(context)            
    

def CardSheet(ls, cardType):
    cards = []
    with open("Input/Lists/" + ls + ".list") as lines:
        for line in lines:
            title, description = (l.strip() for l in line.split(":"))
            cards.append(cardType(title, description))
    with open("Output/" + ls + ".pdf", 'w') as output:
        surface = cairo.PDFSurface(output, 4 * Card.width, 4 * Card.height)
        context = cairo.Context(surface)
        for i in count():
            if i < cards.__len__():
                context.set_source_surface(cards[i].surface, Card.width * i % 4, Card.height * i / 4)
                context.rectangle(Card.width * i % 4, Card.height * i / 4, Card.width, Card.height)
                context.fill()
            else:
                break
        surface.finish()


if __name__ == "__main__":
    CardSheet("objects", Object)
