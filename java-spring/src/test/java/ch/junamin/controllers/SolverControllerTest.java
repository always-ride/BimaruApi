package ch.junamin.controllers;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.http.ResponseEntity;

class SolverControllerTest {

    private SolverController controller;

    @BeforeEach
    void setUp() {
        controller = new SolverController();
    }

    @Test
    void testSolveBimaru_ValidInput() {
        // Gegeben: Eine gültige Spielfeld-Eingabe
        String input = """
            1 | . . . . . . . . . .
            2 | . . . . . . . . . .
            3 | . . . . . . . . . .
            3 | . . . . . . . . □ .
            0 | . . . . . . . . . .
            4 | . . . . . . . . . .
            1 | . . . . . . . . . .
            3 | . ^ . . . . . . . .
            2 | . . . . . . . . v .
            1 | . . . . . . . . . .
                1 6 1 1 2 0 3 1 3 2""";

        // Wenn: Der Solver aufgerufen wird
        ResponseEntity<String> response = controller.solveBimaru(input);

        // Dann: Sollte eine Lösung zurückgegeben werden
        assertNotNull(response);
        assertEquals(200, response.getStatusCode().value());
        assertTrue(response.getBody().contains("|")); // Prüft, ob das Format korrekt ist
    }

    @Test
    void testSolveBimaru_InvalidInput() {
        // Gegeben: Eine fehlerhafte Eingabe
        String invalidInput = "Ungültige Daten";

        // Wenn: Der Solver aufgerufen wird
        ResponseEntity<String> response = controller.solveBimaru(invalidInput);

        // Dann: Sollte ein Fehler zurückgegeben werden
        assertNotNull(response);
        assertEquals(400, response.getStatusCode().value());
        assertEquals("Fehler beim Verarbeiten der Anfrage.", response.getBody());
    }
}
