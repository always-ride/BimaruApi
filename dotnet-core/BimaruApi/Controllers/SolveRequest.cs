namespace BimaruApi.Controllers
{
    public class SolveRequest
    {
        public string[] BoardLines { get; set; } = [];  

        public string Board => string.Join("\n", BoardLines);
    }
}