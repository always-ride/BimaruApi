import cv2
from domain.constraint import Constraint
from domain.grid import Grid


class Board:
    """ Verwaltet das gesamte Spielfeld und extrahiert den Spielzustand. """

    def __init__(self, image_path):
        gray, equalized, binary = self.preprocess_image(image_path)
        self.save_images(gray, equalized, binary)

        self.grid = Grid(equalized, binary)
        self.grid.save_images()

        grid_size = self.grid.get_grid_size()
        grid_box = self.grid.get_bounding_box()
        self.constr = Constraint(gray, grid_box, grid_size)
        self.constr.save_region_images()

    @staticmethod
    def preprocess_image(image_path):
        """ Lädt das Bild und verarbeitet es für die Analyse. """
        gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        equalized = cv2.equalizeHist(gray)
        binary = cv2.adaptiveThreshold(equalized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 1)    
        return gray, equalized, binary
    
    @staticmethod
    def save_images(gray, equalized, binary):
        """ Speichern der Bilder zur Kontrolle """
        cv2.imwrite("./log/gray.png", gray)
        cv2.imwrite("./log/equalized.png", equalized)
        cv2.imwrite("./log/binary.png", binary)  

    def extract_board_as_text(self):
        """ Erstellt die textuelle Repräsentation des Boards. """
        size = self.grid.get_grid_size()
        grid = self.grid.get_bounding_box()
        rows_text = self.constr.extract_rows_text()
        cols_text = self.constr.extract_cols_text()
        
        board_matrix = [["." for _ in range(size)] for _ in range(size)]
        for cell in self.grid.cells:
            box = cell.box
            row = (box.y - grid.y) // box.h
            col = (box.x - grid.x) // box.w
            board_matrix[row][col] = cell.detect_symbol()

        board_lines = []
        for i, row in enumerate(board_matrix):
            board_lines.append(f"{rows_text[i]} | {' '.join(row)}")
        board_lines.append("    " + " ".join(cols_text))
    
        return "\n".join(board_lines)