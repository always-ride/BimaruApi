using BimaruApi.Domain;
using Microsoft.AspNetCore.Mvc;

namespace BimaruApi.Controllers
{
    [Route("api")]
    [ApiController]
    public class SolverController : ControllerBase
    {
        [HttpGet("home")]
        public IActionResult Home() 
        {
            return Ok("Hello Bimaru Universe of dotnet-core!");
        }

        [HttpPost("solve")]
        [Consumes("text/plain")]
        public async Task<IActionResult> SolveBimaru()
        {
            try
            {
                using var reader = new StreamReader(Request.Body);
                var requestBody = await reader.ReadToEndAsync();

                if (string.IsNullOrWhiteSpace(requestBody))
                {
                    return BadRequest("Leerer Request-Body ist nicht erlaubt.");
                }
                
                Board board = new(requestBody);
                Solver solver = new(board);
                solver.Solve();
                var solutions = solver.GetUniqueSolutions();

                return Ok(solutions.Count > 0
                    ? string.Join("\n\n", solutions) 
                    : "Keine Lösung gefunden.");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Fehler beim Verarbeiten der Anfrage: {ex.Message}");
                return BadRequest("Fehler beim Verarbeiten der Anfrage.");
            }
        }

        [HttpPost("solve/json")]
        [Consumes("application/json")]
        public IActionResult SolveBimaruJson([FromBody] SolveRequest request)
        {
            try
            {
                if (string.IsNullOrWhiteSpace(request.Board))
                {
                    return BadRequest("Das Board darf nicht leer sein.");
                }

                Board board = new(request.Board);
                Solver solver = new(board);
                solver.Solve();
                var solutions = solver.GetUniqueSolutions();

                return Ok(solutions.Count > 0
                    ? new { solutions = solutions.Select(s => s.Split('\n')).ToArray() } 
                    : new { info = "Keine Lösung gefunden." });
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Fehler beim Verarbeiten der Anfrage: {ex.Message}");
                return BadRequest(new { error = "Fehler beim Verarbeiten der Anfrage.", details = ex.Message });
            }
        }
    }
}
