package ch.junamin.domain;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Solver {
    private final ISolvableBoard board;
    private final int[][] ships;
    private final Set<String> uniqueSolutions;
    private int solutionsCount;

    public Solver(ISolvableBoard board) {
        this.board = board;
        this.ships = new int[][]{{4, 1}, {3, 2}, {2, 3}, {1, 4}};
        this.uniqueSolutions = new HashSet<>();
    }

    public boolean solve() {
        board.resetBoard();
        uniqueSolutions.clear();
        solutionsCount = 0;
        solve(0, 0, 0, 0); // Starte mit dem ersten Schiff an Position (0,0)
        return !uniqueSolutions.isEmpty();
    }

    private void solve(int shipIndex, int placedCount, int startRow, int startCol) {
        if (shipIndex == ships.length) {
            if (board.isValidSolution()) {
                uniqueSolutions.add(board.asText());
                solutionsCount++;
            }
            return;
        }

        int size = ships[shipIndex][0];
        int count = ships[shipIndex][1];

        if (placedCount == count) {
            // Alle Schiffe dieser Grösse platziert → nächster Schiffstyp
            solve(shipIndex + 1, 0, 0, 0);
            return;
        }

        for (int row = startRow; row < board.getSize(); row++) {
            for (int col = (row == startRow ? startCol : 0); col < board.getSize(); col++) {
                char[] directions = (size == 1)
                        ? new char[]{'H'} // Einer-Schiff ausschliesslich horizontal platzieren
                        : new char[]{'H', 'V'};
                for (char direction : directions) {
                    if (board.canPlaceShip(row, col, size, direction)) {
                        board.placeShip(row, col, size, direction);
                        solve(shipIndex, placedCount + 1, row, col); // Weiter mit gleicher Grösse
                        board.removeShip(row, col, size, direction);
                    }
                }
            }
        }
    }

    public List<String> getUniqueSolutions() { return uniqueSolutions.stream().toList(); }
    public int getSolutionsCount() { return solutionsCount; }
}
