package ch.junamin.models;

public class Cell {
    int row, col;
    char value;

    public Cell(int row, int col, char value) {
        this.row = row;
        this.col = col;
        this.value = value;
    }

    @Override
    public String toString() {
        return value + "(" + row + "," + col + ")";
    }
}
