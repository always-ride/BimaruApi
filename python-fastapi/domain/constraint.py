import cv2
import pytesseract
from domain.bounding_box import BoundingBox


class Constraint:
    """ Verwaltet die Extraktion der Zeilen- und Spalten-Constraints. """

    def __init__(self, image, grid: BoundingBox, size):
        self.size = size
        self.rows_region, self.cols_region = Constraint.detect_regions(image, grid, size)

    def extract_rows_text(self):
        return Constraint.extract_text(self.rows_region, self.size)

    def extract_cols_text(self):
        return Constraint.extract_text(self.cols_region, self.size)
    
    def save_region_images(self):
        """ Speichern der Ausschnitte zur Kontrolle """
        cv2.imwrite('./log/constraint_of_rows.png', self.rows_region)
        cv2.imwrite('./log/constraint_of_cols.png', self.cols_region)
    
    @staticmethod
    def detect_regions(image, grid, size):
        height, width = image.shape  # Bildgrösse
        cell_width = grid.w // size
        cell_height = grid.h // size
        shift_factor = 0.14

        # Vertikale Constraints (Spaltenbeschriftungen unterhalb des Grids)
        col_x1 = grid.x
        col_x2 = grid.x + grid.w
        col_y1 = grid.y + grid.h + round(cell_height * shift_factor)
        col_y2 = min(col_y1 + cell_height, height)  # Unterhalb des Grids
        col_constraints_region = image[col_y1:col_y2, col_x1:col_x2]

        # Horizontale Constraints (Zeilenbeschriftungen rechts neben dem Grid)
        row_x1 = grid.x + grid.w + round(cell_width * shift_factor)  # Rechts neben dem Grid
        row_x2 = min(row_x1 + cell_width, width)  # Maximalbreite des Bildes
        row_y1 = grid.y
        row_y2 = grid.y + grid.h
        row_constraints_region = image[row_y1:row_y2, row_x1:row_x2]

        return row_constraints_region, col_constraints_region

    @staticmethod
    def extract_text(region, size):
        text = ""
        height, width = region.shape   
        length = max(height, width)
        split_length = length // size
        
        for i in range(size):
            start = i * split_length
            end = min((i + 1) * split_length, length)
            
            if height > width:  # Vertikale Zerteilung
                sub_region = region[start:end, :]
            else:  # Horizontale Zerteilung
                sub_region = region[:, start:end]

            part_text = pytesseract.image_to_string(
                sub_region, 
                config='--psm 6 -c tessedit_char_whitelist=0123456789')
            text += part_text.strip().replace('\n', '')

        return text