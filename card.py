
from cairo import Context, PDFSurface
from cairo import LINE_JOIN_ROUND as rounded
from pangocairo import CairoContext
import pango
from pango import FontDescription
from rsvg import Handle as SVG
from StringIO import StringIO

class Card:
    font = "Quicksand Book"

    def __init__(self, title, description, width, height):
        self.description = description
        self.processName(title)
        self.w, self.h = width, height
        self.loadSVG()

    def processName(self, text):
        self.title = text.upper()
        self.name = text

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
            self.renderText(surface, self.title, self.h * 2 / 5, self.w / 16, 0, wrap=False)
            self.renderText(surface, self.description, self.h / 2, self.w / 32, 0.1)
        else:
            self.renderText(surface, self.title, self.h * 4 / 9, self.w / 14, 0, wrap=False)

    def renderText(self, surface, text, y_offset, size, shade, w=(5,9), wrap=True):
        if len(text) < 1:
            return
        
        def setdesc(l, size):
            l.set_font_description(FontDescription(self.font + " " + str(size)))
        
        origin = Context(surface)
        origin.translate(self.w * (w[1] - w[0]) / (w[1] * 2), y_offset)
        box = CairoContext(origin)
        layout = box.create_layout()
        setdesc(layout, size)
        width = self.w * w[0] / w[1]
        if wrap:
            layout.set_width(width * pango.SCALE)
        else:
            layout.set_width(-1)
        layout.set_alignment(pango.ALIGN_CENTER)
        layout.set_justify(True)
        layout.set_text(text)

        wi, n = layout.get_pixel_size()
        if wi > width:
            s = size * width / wi
            setdesc(layout, s)
        layout.set_width(width * pango.SCALE)
        origin.set_source_rgba(1, 1, 1, 0.7)
        origin.rectangle(*layout.get_pixel_extents()[1])
        origin.fill()
        origin.set_source_rgb(shade, shade, shade)
        box.update_layout(layout)
        box.show_layout(layout)

    def loadSVG(self):
        if len(self.name) > 0:
            svg_name = "Input/" + self.__class__.__name__ + "/" + self.name + ".svg"
            try:
                self.art = SVG(file=svg_name)
            except:
                print "Error processing", svg_name
                self.art = None

