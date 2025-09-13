import cv2


class BaseRegion:
    """ Basisklasse für Regionen mit Bildausschnitten und Konturenerkennung. """

    def __init__(self, image, thresh):
        self.image = image
        self.thresh = thresh

    def find_contours(self, inverse=False):
        """ Findet Konturen in der binarisierten Darstellung. """
        thresh = cv2.bitwise_not(self.thresh) if inverse else self.thresh
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def draw_contours(self, output_path="contours.png"):
        """ Zeichnet Konturen auf das Bild und speichert es. """
        contour_image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(contour_image, self.find_contours(), -1, (0, 0, 255), 1)
        cv2.imwrite(output_path, contour_image)