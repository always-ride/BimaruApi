import cv2
import numpy as np
import pytesseract
from domain.grid import Grid


class Board:
    """ Verwaltet das gesamte Spielfeld und extrahiert den Spielzustand. """

    def __init__(self, image_path):
        self.image, self.thresh = self.preprocess_image(image_path)
        self.grid = Grid(self.image, self.thresh)
        self.grid.detect_cells_and_size()

    @staticmethod
    def preprocess_image(image_path):
        """ Lädt das Bild und verarbeitet es für die Analyse. """
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        image = cv2.equalizeHist(image)
        thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 1)
        return image, thresh

    def extract_board(self):
        """ Erstellt die textuelle Repräsentation des Boards. """
        size = self.grid.get_grid_size()
        board_matrix = [["." for _ in range(size)] for _ in range(size)]

        # Bestimme die obere linke Ecke des Grids
        grid_x = min(cell.x for cell in self.grid.cells)
        grid_y = min(cell.y for cell in self.grid.cells)

        for cell in self.grid.cells:
            row = (cell.y - grid_y) // cell.h
            col = (cell.x - grid_x) // cell.w
            board_matrix[row][col] = cell.detect_symbol()

        # Bestimme Grid-Abmessung (Shape)
        grid_w = max(cell.x + cell.w for cell in self.grid.cells) - grid_x
        grid_h = max(cell.y + cell.h for cell in self.grid.cells) - grid_y

        constraints = self.extract_constraints(grid_x, grid_y, grid_w, grid_h)
    
        board_lines = []
        for i, row in enumerate(board_matrix):
            board_lines.append(f"{constraints['rows'][i]} | {' '.join(row)}")
        board_lines.append("    " + " ".join(constraints["cols"]))
    
        return "\n".join(board_lines)

    def extract_constraints(self, grid_x, grid_y, grid_w, grid_h):
        size = self.grid.get_grid_size()
        constraints = {"rows": [], "cols": []}
        cell_height = grid_h // size
        cell_width = grid_w // size
        d = 8

        def clean_thresh_morph(thresh):
            kernel = np.ones((2, 2), np.uint8)
            return cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)

        clean = clean_thresh_morph(self.thresh)
 
        # Kopie des Bildes für die Visualisierung
        vis_img = cv2.cvtColor(clean.copy(), cv2.COLOR_GRAY2BGR)  # Falls das Bild grau ist, konvertieren

        def extract_number(cell, x_offset, y_offset):
            """Findet die relevante Zahl in der Zelle und gibt den OCR-Text zurück."""
            gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY) if len(cell.shape) == 3 else cell
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # # Bounding Box im Visualisierungsbild einzeichnen (Offset hinzufügen)
            # g_w, g_h = gray.shape
            # cv2.rectangle(vis_img, (x_offset, y_offset), 
            #             (x_offset + g_w, y_offset + g_h), (0, 0, 255), 1)
            
            if contours:
                d = 2
                x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))  # Größte Kontur nehmen
                x, y, w, h = x-d, y-d, w+2*d, h+2*d
                if x < 0: x = 0
                if y < 0: y = 0
                roi = cell[y:y+h, x:x+w]  # ROI auf Bereich der Kontur zuschneiden
                text = pytesseract.image_to_string(roi, config='--psm 10 -c tessedit_char_whitelist=0123456789').strip()
            
                # Bounding Box im Visualisierungsbild einzeichnen (Offset hinzufügen)
                cv2.rectangle(vis_img, (x_offset + x, y_offset + y), 
                            (x_offset + x + w, y_offset + y + h), (0, 255, 0), 1)
                
                return text if text else "0"
            return "0"

        # Reihen (rechts neben dem Raster)
        for i in range(size):
            y = d + grid_y + i * cell_height
            x = d + grid_x + grid_w
            row_cell = clean[y:y+cell_height-2*d, x:x+cell_width-2*d]
            constraints["rows"].append(extract_number(row_cell, x, y))

        # Spalten (unter dem Raster)
        for i in range(size):
            x = d + grid_x + i * cell_width
            y = d + grid_y + grid_h
            col_cell = clean[y:y+cell_height-2*d, x:x+cell_width-2*d]
            constraints["cols"].append(extract_number(col_cell, x, y))

        cv2.imwrite("./log/constraints.png", vis_img)

        return constraints
