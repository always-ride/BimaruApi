import cv2
import numpy as np
from domain.base_region import BaseRegion
from domain.bounding_box import BoundingBox


class Cell:
    """Repräsentiert eine einzelne Zelle im Raster."""

    def __init__(self, image, thresh, b: BoundingBox):
        self.br = BaseRegion(
            image[b.y : b.y + b.h, b.x : b.x + b.w], 
            thresh[b.y : b.y + b.h, b.x : b.x + b.w]
        )
        self.box = b

    def analyze_brightness(self):
        """Analysiert die Helligkeitsverteilung innerhalb der Zelle."""
        return np.mean(self.br.image)

    def detect_symbol(self):
        """Bestimmt das Symbol innerhalb der Zelle."""
        brightness = self.analyze_brightness()
        if brightness > 210:
            return "."

        contours = self.br.find_contours(inverse=True)
        if not contours:
            return "."

        if len(contours) >= 3:
            areas = sorted([cv2.contourArea(c) for c in contours], reverse=True)[:3]
            if max(areas) - min(areas) <= 0.1 * max(areas):
                return "~"

        aspect_ratio = self.box.w / float(self.box.h)
        if 0.9 < aspect_ratio < 1.1:
            return self.determine_ship_part()
        else:
            return "#"

    def determine_ship_part(self):
        brightness = self.analyze_brightness_distribution()

        # Helligkeitswerte in binäre Werte umwandeln
        bright_regions = brightness > 90

        if np.array_equal(bright_regions, np.array([
            [False, False, False], 
            [False, False, False],
            [False, False, False]])):
            return "□"  # Mittelteil
        elif np.array_equal(bright_regions, np.array([
            [True, False, False], 
            [False, False, False], 
            [True, False, False]])):
            return "<"  # Links
        elif np.array_equal(bright_regions, np.array([
            [False, False,  True], 
            [False, False, False], 
            [False, False,  True]])):
            return ">"  # Rechts
        elif np.array_equal(bright_regions, np.array([
            [ True, False,  True], 
            [False, False, False], 
            [False, False, False]])):
            return "^"  # Oben
        elif np.array_equal(bright_regions, np.array([
            [False, False, False], 
            [False, False, False], 
            [ True, False,  True]])):
            return "v"  # Unten
        elif np.array_equal(bright_regions, np.array([
            [ True, False,  True], 
            [False, False, False], 
            [ True, False,  True]])):
            return "o"  # U-Boot
        else:
            return "s"

    def analyze_brightness_distribution(self):
        cell = self.br.image
        h, w = cell.shape
        grid_size = 3
        cell_h, cell_w = h // grid_size, w // grid_size
        brightness = np.zeros((grid_size, grid_size))

        for i in range(grid_size):
            for j in range(grid_size):
                sub_cell = cell[i*cell_h : (i+1)*cell_h, j*cell_w : (j+1)*cell_w]
                brightness[i, j] = np.mean(sub_cell)

        return brightness

    def __repr__(self):
        return f"{self.box.x}|{self.box.y}"
