package ch.junamin.domain;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class Board implements ISolvableBoard {
    protected final int SIZE;
    protected final char[][] grid;
    protected final int[] rowConstraints;
    protected final int[] colConstraints;
    private final List<Cell> initialCells;

    public Board(String puzzle) {
        this(puzzle, 10);
    }

    protected Board(String puzzle, int size) {
        SIZE = size;
        grid = new char[SIZE][SIZE];
        rowConstraints = new int[SIZE];
        colConstraints = new int[SIZE];
        initialCells = new ArrayList<>();
        parseInput(puzzle);
    }

    private void parseInput(String puzzle) {
        String[] lines = puzzle.split("\n");
        for (int i = 0; i < SIZE; i++) {
            String[] parts = lines[i].split("\\|");
            rowConstraints[i] = Integer.parseInt(parts[0].trim());
            String[] rowValues = parts[1].trim().split(" ");
            for (int j = 0; j < SIZE; j++) {
                grid[i][j] = rowValues[j].charAt(0);
                if (grid[i][j] != '.') {
                    initialCells.add(new Cell(i, j, grid[i][j]));
                }
            }
        }
        String[] colValues = lines[SIZE].trim().split(" ");
        for (int j = 0; j < SIZE; j++) {
            colConstraints[j] = Integer.parseInt(colValues[j]);
        }
    }

    @Override
    public void resetBoard() {
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                grid[i][j] = '.';
            }
        }
    }

    @Override
    public boolean canPlaceShip(int row, int col, int size, char direction) {
        if (direction != 'H' && direction != 'V') return false;
        boolean isHorizontal = direction == 'H';

        int maxIndex = isHorizontal ? col + size : row + size;
        if (maxIndex > SIZE) return false;

        int[] constraints = isHorizontal ? rowConstraints : colConstraints;
        int num = isHorizontal ? row : col;

        if (constraints[num] - countShipCells(num, isHorizontal) < size) return false;

        int[] opposingConstraints = isHorizontal ? colConstraints : rowConstraints;
        for (int i = 0; i < size; i++) {
            int r = isHorizontal ? row : row + i;
            int c = isHorizontal ? col + i : col;

            if (r >= SIZE || c >= SIZE || grid[r][c] != '.') return false;

            int index = isHorizontal ? col + i : row + i;
            if (opposingConstraints[index] - countShipCells(index, !isHorizontal) < 1) return false;

            // Prüfe umliegende Zellen
            for (int dr = -1; dr <= 1; dr++) {
                for (int dc = -1; dc <= 1; dc++) {
                    int nr = r + dr;
                    int nc = c + dc;
                    if (nr >= 0 && nr < SIZE && nc >= 0 && nc < SIZE) {
                        if (grid[nr][nc] != '.' && grid[nr][nc] != '~') return false;
                    }
                }
            }
        }

        return true;
    }

    private int countShipCells(int index, boolean isRow) {
        int count = 0;
        for (int i = 0; i < SIZE; i++) {
            char cell = isRow ? grid[index][i] : grid[i][index];
            if (cell != '.' && cell != '~') count++;
        }
        return count;
    }

    private static String getShipRepresentation(int size, char direction) {
        if (size == 1) return "o"; // Kein Austausch nötig!

        String middle = "□".repeat(Math.max(0, size - 2));
        String ship = "<" + middle + ">";

        return (direction == 'H') ? ship : ship.replace("<", "^").replace(">", "v");
    }

    @Override
    public void placeShip(int row, int col, int size, char direction) {
        if (!canPlaceShip(row, col, size, direction)) return;
        String representation = getShipRepresentation(size, direction);
        for (int i = 0; i < size; i++) {
            int r = row + (direction == 'V' ? i : 0);
            int c = col + (direction == 'H' ? i : 0);
            grid[r][c] = representation.charAt(i);
        }
    }

    @Override
    public void removeShip(int row, int col, int size, char direction) {
        if (size == 1) {
            grid[row][col] = '.';
            return;
        }
        for (int i = 0; i < size; i++) {
            int r = direction == 'H' ? row : row + i;
            int c = direction == 'H' ? col + i : col;
            grid[r][c] = '.';
        }
    }

    @Override
    public boolean isValidSolution() {
        for (Cell cell : initialCells) {
            char value = grid[cell.row][cell.col];
            char valueCell = cell.value == '~'
                    ? '.' // Behandle Wasser wie leere Zelle
                    : cell.value;
            if (value != valueCell)
                return false;
        }
        return true;
    }

    public int getSize() { return SIZE; }

    public String asText() {
        String board = IntStream.range(0, rowConstraints.length)
            .mapToObj(i -> rowConstraints[i] + " | " + 
                String.join(" ", new String(grid[i]).split("")))
            .collect(Collectors.joining("\n"));

        String constraints = "    " + Arrays.stream(colConstraints)
            .mapToObj(String::valueOf)
            .collect(Collectors.joining(" "));

        return (board + "\n" + constraints).replace('.', '~');
    }
}
