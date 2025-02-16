package ch.junamin.domain;

public interface ISolvableBoard {
    void resetBoard();

    boolean canPlaceShip(int row, int col, int size, char direction);

    void placeShip(int row, int col, int size, char direction);

    void removeShip(int row, int col, int size, char direction);

    boolean isValidSolution();

    int getSize();

    String asText();
}
