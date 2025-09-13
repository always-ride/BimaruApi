import pytest
from app import App

@pytest.mark.parametrize("image, expected_board", [
    ("bimaru_6x6.png", """. ~ . ~ . ~
~ ~ . ~ □ ~
o ~ . ~ v ~
~ ~ ~ ~ ~ ~
o ~ < □ > ~
~ ~ ~ ~ ~ ~"""),
    ("solve_request_3.png", """. . . . . . . . .
. . . . . . . . .
. . . . . . < . .
. . . . . . . . .
. . . . < . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . ."""),
])
def test_bimaru_from_image(image, expected_board):
    assert App.bimaru_from_image(image) == expected_board
