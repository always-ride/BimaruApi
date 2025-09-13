import cv2
from domain.grid import Grid


class Board:
    """ Verwaltet das gesamte Spielfeld und extrahiert den Spielzustand. """

    def __init__(self, image_path):
        self.image, self.thresh = self.preprocess_image(image_path)
        self.grid = Grid(self.image, self.thresh)
        self.grid.detect_cells()

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
        grid_x_min = min(cell.x for cell in self.grid.cells)
        grid_y_min = min(cell.y for cell in self.grid.cells)

        for cell in self.grid.cells:
            row = (cell.y - grid_y_min) // cell.h
            col = (cell.x - grid_x_min) // cell.w
            board_matrix[row][col] = cell.detect_symbol()

        return "\n".join(" ".join(row) for row in board_matrix)