import pytest
from app import App

@pytest.mark.parametrize("image, expected_board", [
    ("bimaru_6x6.png", """2 | . ~ . ~ . ~
2 | ~ ~ . ~ □ ~
2 | o ~ . ~ v ~
0 | ~ ~ ~ ~ ~ ~
4 | o ~ < □ > ~
0 | ~ ~ ~ ~ ~ ~
    3 0 3 1 3 0"""),
    ("solve_request_3.png", """2 | . . . . . . . . .
1 | . . . . . . . . .
4 | . . . . . . < . .
2 | . . . . . . . . .
3 | . . . . < . . . .
1 | . . . . . . . . .
4 | . . . . . . . . .
2 | . . . . . . . . .
1 | . . . . . . . . .
    3 2 1 4 1 3 1 4 1"""),
])
def test_bimaru_from_image(image, expected_board):
    assert App.bimaru_from_image(image) == expected_board
