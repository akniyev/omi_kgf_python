import math
from typing import Set

from PyQt5.QtGui import QPainter, QPen, QColor

import PlotLab.Classes.View.HandleItem as ha
from PlotLab.Classes.View.DiagramItem import DiagramItem, DragType
from PlotLab.Classes.View.NodeItem import NodeItem


class LineItem(DiagramItem):
    def __init__(self):
        super().__init__()
        self.movable = DragType.Immovable
        self.source: ha.HandleItem = None
        self.destination: ha.HandleItem = None

    def remove(self):
        s = self.source
        d = self.destination
        if s is not None and d is not None:
            if self in s.output_lines:
                s.output_lines.remove(self)
            d.input_line = None
            if d.parent is not None:
                d.parent.invalidate_node()

    def set_ends(self, s: ha.HandleItem, d: ha.HandleItem):
        if s.parent is not None and d.parent is not None and self.no_cycle(d.parent, set([s.parent])):
            if d.input_line is None and self not in s.output_lines and s.parent != d.parent:
                d.input_line = self
                s.output_lines.add(self)
                self.source = s
                self.destination = d

    def draw(self, qp: QPainter):
        if self.source is None or self.destination is None:
            return
        p1 = self.source.global_center()
        p2 = self.destination.global_center()
        pen = QPen(QColor("black") if not self.selected else QColor(100, 100, 200))
        pen.setWidth(1 if not (self.hover or self.selected) else 3)
        qp.setPen(pen)
        qp.drawLine(p1, p2)

    @staticmethod
    def line_magnitude(x1, y1, x2, y2):
        line_magnitude = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
        return line_magnitude

    # Calc minimum distance from a point and a line segment (i.e. consecutive vertices in a polyline).
    def distance_point_line(self, px, py, x1, y1, x2, y2):
        # http://local.wasp.uwa.edu.au/~pbourke/geometry/pointline/source.vba
        line_mag = self.line_magnitude(x1, y1, x2, y2)

        if line_mag < 0.00000001:
            distance_point_line = 9999
            return distance_point_line

        u1 = (((px - x1) * (x2 - x1)) + ((py - y1) * (y2 - y1)))
        u = u1 / (line_mag * line_mag)

        if (u < 0.00001) or (u > 1):
            # // closest point does not fall within the line segment, take the shorter distance
            # // to an endpoint
            ix = self.line_magnitude(px, py, x1, y1)
            iy = self.line_magnitude(px, py, x2, y2)
            if ix > iy:
                distance_point_line = iy
            else:
                distance_point_line = ix
        else:
            # Intersecting point is on the line, use the formula
            ix = x1 + u * (x2 - x1)
            iy = y1 + u * (y2 - y1)
            distance_point_line = self.line_magnitude(px, py, ix, iy)

        return distance_point_line

    def point_hit_check(self, x, y):
        if self.source is None or self.destination is None:
            return False
        p1 = self.source.global_center()
        p2 = self.destination.global_center()
        min_dist = 3
        return self.distance_point_line(x, y, p1.x(), p1.y(), p2.x(), p2.y()) < min_dist

    def no_cycle(self, node: NodeItem, past_items: Set[NodeItem]) -> bool:
        if node in past_items:
            return False
        result = True
        for output in node.output_handlers:
            for line in output.output_lines:
                if line.destination is not None and line.destination.parent is not None:
                    d = line.destination.parent
                    result = result and self.no_cycle(d, past_items.union([node]))
        return result


