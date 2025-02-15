package ch.junamin.controllers;

import java.util.List;

import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import ch.junamin.models.Board;
import ch.junamin.services.Solver;

@RestController
@RequestMapping("/api")
@SpringBootApplication
public class SolverController {

    @PostMapping("/solve")
    public ResponseEntity<String> solveBimaru(@RequestBody String requestBody) {
        try {
            Board board = new Board(requestBody);
            Solver solver = new Solver(board);
            solver.solve();
            List<String> solutions = solver.getUniqueSolutions();
            String response = String.join("\n\n", solutions);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Fehler beim Verarbeiten der Anfrage.");
        }
    }
}