namespace BimaruApi.Controllers
{
    public class SolveRequest
    {
        public string[] BoardLines { get; set; } = Array.Empty<string>();  

        public string Board => string.Join("\n", BoardLines);
    }
}