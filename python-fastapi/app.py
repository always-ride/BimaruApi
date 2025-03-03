from domain.board import Board


class App:
    @staticmethod
    def bimaru_from_image(image_path):
        board = Board("./doc/" + image_path)
        return board.extract_board()


if __name__ == "__main__":
    image_path = "solve_request_3.png"
    # image_path = "bimaru_6x6.png"
    print(App.bimaru_from_image(image_path))
