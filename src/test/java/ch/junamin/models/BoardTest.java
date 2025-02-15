package ch.junamin.models;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.*;

public class BoardTest {
    @Test
    public void testParseInput() {
        var sut = new TestableBoard("""
                6 | . . . . . . . . ~ .
                0 | . . . . . . . . . .
                1 | . . . . . . . . . .
                0 | . . . . . . . . . .
                2 | . . . . . . . . . .
                3 | . . . . . . . . < .
                0 | . . . . . . . . . .
                2 | . . . . . . . . . .
                3 | . ~ . . . . . . . .
                3 | . . . . . . . . . .
                    3 4 1 4 2 0 1 0 3 2""");

        assertArrayEquals(new int[]{6, 0, 1, 0, 2, 3, 0, 2, 3, 3}, sut.getRowConstraints());
        assertArrayEquals(new int[]{3, 4, 1, 4, 2, 0, 1, 0, 3, 2}, sut.getColConstraints());
    }

    @ParameterizedTest
    @CsvSource({
            "0, 2, 1, H, true",
            "0, 6, 1, H, false",
            "0, 3, 3, H, true",
            "0, 4, 3, H, false",
            "2, 5, 1, H, true",
            "2, 5, 1, V, true",
    })
    public void testCanPlaceShip(int row, int col, int length, char direction, boolean expected) {
        var sut = new TestableBoard(SIMPLE_BOARD);
        assertEquals(expected, sut.canPlaceShip(row, col, length, direction));
    }

    @ParameterizedTest
    @CsvSource({
            "0, 2, 3, H, '3 | . . < □ > . . . . .'",
            "2, 5, 1, V, '6 | < □ □ > . o . . o .'",
    })
    public void testPlaceShip(int row, int col, int length, char direction, String expected) {
        var sut = new TestableBoard(SIMPLE_BOARD);
        sut.placeShip(row, col, length, direction);
        assertEquals(expected, sut.getLine(row, 'H').replace("^","<").replace("v",">"));
    }

    private static final String SIMPLE_BOARD =
            "3 | . . . . . . . . . . \n" +
            "0 | . . . . . . . . . . \n" +
            "6 | < □ □ > . . . . o . \n" +
            "0 | . . . . . . . . . . \n".repeat(7) +
            "    1 1 2 2 1 1 0 0 1 0";

    static class TestableBoard extends Board {

        public TestableBoard(String puzzle) {
            super(puzzle, 10);
        }

        public int[] getRowConstraints() { return rowConstraints; }
        public int[] getColConstraints() { return colConstraints; }

        public String getLine(int index, char direction) {
            int constraint = direction == 'H'
                    ? rowConstraints[index]
                    : colConstraints[index];
            var line = new StringBuilder(constraint + " |");
            for (int j = 0; j < SIZE; j++) {
                line.append(direction == 'H'
                        ? " " + grid[index][j]
                        : " " + grid[j][index]);
            }
            return line.toString();
        }
    }
}
