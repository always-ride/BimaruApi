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
    }
}
