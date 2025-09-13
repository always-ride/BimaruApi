import cv2
import numpy as np
from domain.cell import Cell
from domain.base_region import BaseRegion


class Grid(BaseRegion):
    """Erkennt und verwaltet das Raster (Gitter) des Spielfelds."""

    def __init__(self, image, thresh):
        super().__init__(image, thresh)
        self.cells = []

    def detect_cells_and_size(self):
        self.detect_cells()
        self.detect_grid_size()

    def detect_cells(self):
        """Ermittelt die einzelnen Zellen des Rasters."""
        contours = self.find_contours()
        cell_candidates = []

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / float(h)
            H, W = self.thresh.shape
            min, max = 0.05, 0.25
            if (
                0.8 < aspect_ratio < 1.2
                and W * min <= w <= W * max
                and H * min <= h <= H * max
            ):
                cell_candidates.append((x, y, w, h))

        if not cell_candidates:
            raise ValueError("Keine geeigneten Zellen gefunden.")

        # Sortieren nach Position für ein einheitliches Raster
        cell_candidates.sort(key=lambda c: (c[1], c[0]))
        cell_widths = [c[2] for c in cell_candidates]
        cell_heights = [c[3] for c in cell_candidates]

        self.cell_w = int(np.median(cell_widths))
        self.cell_h = int(np.median(cell_heights))

        filtered_cells = [
            c
            for c in cell_candidates
            if abs(c[2] - self.cell_w) <= 2 and abs(c[3] - self.cell_h) <= 2
        ]
        if not filtered_cells:
            raise ValueError("Nach der Filterung keine gültigen Zellen mehr übrig.")

        self.cells = [Cell(self.image, self.thresh, *c) for c in filtered_cells]

    def detect_grid_size(self):
        """Bestimmt die Rastergröße anhand der Zellpositionen."""
        unique_x = []
        unique_y = []
        tolerance = 1

        for c in self.cells:
            cx, cy = c.x + c.w // 2, c.y + c.h // 2
            if not any(abs(cx - ux) <= tolerance for ux in unique_x):
                unique_x.append(cx)
            if not any(abs(cy - uy) <= tolerance for uy in unique_y):
                unique_y.append(cy)

        self.grid_size = round(np.mean([len(unique_x), len(unique_y)]))

    def get_grid_size(self):
         return self.grid_size
