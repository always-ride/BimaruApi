import cv2
import numpy as np
from domain.bounding_box import BoundingBox
from domain.cell import Cell
from domain.base_region import BaseRegion


class Grid:
    """Erkennt und verwaltet das Raster (Gitter) des Spielfelds."""

    def __init__(self, image, thresh):
        self.parent = BaseRegion(image, thresh)
        self.cells = self.detect_cells()
        self.size = self.detect_grid_size()

    def save_images(self):
        """Grid einzeichnen zur Kontrolle."""
        grid = self.get_bounding_box()
        pt1 = (grid.x, grid.y)  # Obere linke Ecke
        pt2 = (grid.x + grid.w, grid.y + grid.h)  # Untere rechte Ecke
        found_grid = cv2.cvtColor(self.parent.image, cv2.COLOR_GRAY2BGR)
        cv2.rectangle(found_grid, pt1, pt2, (0, 255, 0), 1)  # Grüne Box mit Dicke 1
        cv2.imwrite("./log/found_grid.png", found_grid)

    def detect_cells(self):
        """Ermittelt die einzelnen Zellen des Rasters."""
        contours = self.parent.find_contours()
        cell_candidates = []

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            box = BoundingBox(x, y, w, h)
            aspect_ratio = w / float(h)
            H, W = self.parent.thresh.shape
            min, max = 0.05, 0.25
            if (
                0.8 < aspect_ratio < 1.2
                and W * min <= w <= W * max
                and H * min <= h <= H * max
            ):
                cell_candidates.append(box)

        if not cell_candidates:
            raise ValueError("Keine geeigneten Zellen gefunden.")

        # Sortieren nach Position für ein einheitliches Raster
        cell_candidates.sort(key=lambda c: (c.y, c.y))
        cell_widths = [c.w for c in cell_candidates]
        cell_heights = [c.h for c in cell_candidates]

        self.cell_w = int(np.median(cell_widths))
        self.cell_h = int(np.median(cell_heights))

        filtered_cells = [
            box
            for box in cell_candidates
            if abs(box.w - self.cell_w) <= 2 and abs(box.h - self.cell_h) <= 2
        ]
        if not filtered_cells:
            raise ValueError("Nach der Filterung keine gültigen Zellen mehr übrig.")

        return [Cell(self.parent.image, self.parent.thresh, box) for box in filtered_cells]

    def detect_grid_size(self):
        """Bestimmt die Rastergröße anhand der Zellpositionen."""
        unique_x = []
        unique_y = []
        tolerance = 1

        for c in self.cells:
            b = c.box
            cx, cy = b.x + b.w // 2, b.y + b.h // 2
            if not any(abs(cx - ux) <= tolerance for ux in unique_x):
                unique_x.append(cx)
            if not any(abs(cy - uy) <= tolerance for uy in unique_y):
                unique_y.append(cy)

        return round(np.mean([len(unique_x), len(unique_y)]))

    def get_grid_size(self):
         return self.size
    
    def get_bounding_box(self):
        box_list = list(map(lambda c: c.box, self.cells))

        # Bestimme die obere linke Ecke des Grids
        grid_x = min(b.x for b in box_list)
        grid_y = min(b.y for b in box_list)

        # Bestimme Grid-Abmessung (Shape)
        grid_w = max(b.x + b.w for b in box_list) - grid_x
        grid_h = max(b.y + b.h for b in box_list) - grid_y

        return BoundingBox(grid_x, grid_y, grid_w, grid_h)

