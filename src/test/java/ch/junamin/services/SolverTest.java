package ch.junamin.services;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;
import java.util.List;

import ch.junamin.models.Board;

public class SolverTest {
    @Test
    public void testSolve() {
        Solver sut = new Solver(new Board("""
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
                3 4 1 4 2 0 1 0 3 2"""));
        assertTrue(sut.solve());
        List<String> solutions = sut.getUniqueSolutions();
        assertEquals(1, sut.getSolutionsCount());
        assertEquals(1, solutions.size());
        assertEquals("""
            6 | ~ < □ □ > ~ o ~ ~ o
            0 | ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
            1 | ~ o ~ ~ ~ ~ ~ ~ ~ ~
            0 | ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
            2 | ~ ^ ~ ~ o ~ ~ ~ ~ ~
            3 | ~ v ~ ~ ~ ~ ~ ~ < >
            0 | ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
            2 | ^ ~ ~ ^ ~ ~ ~ ~ ~ ~
            3 | □ ~ ~ □ ~ ~ ~ ~ ^ ~
            3 | v ~ ~ v ~ ~ ~ ~ v ~
                3 4 1 4 2 0 1 0 3 2""", solutions.get(0));//.getFirst());
    }
}