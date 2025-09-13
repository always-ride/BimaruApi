namespace BimaruApi.Domain
{
    public class Solver(ISolvableBoard board)
    {
        private readonly ISolvableBoard board = board;
        private readonly int[][] ships = board.Ships;
        private readonly HashSet<string> uniqueSolutions = [];
        private int solutionsCount;

        public bool Solve()
        {
            board.ResetBoard();
            uniqueSolutions.Clear();
            solutionsCount = 0;
            Solve(0, 0, 0, 0);
            return uniqueSolutions.Count > 0;
        }

        private void Solve(int shipIndex, int placedCount, int startRow, int startCol)
        {
            if (shipIndex == ships.Length)
            {
                if (board.IsValidSolution())
                {
                    uniqueSolutions.Add(board.AsText.Replace('.', '~'));
                    solutionsCount++;
                }
                return;
            }

            int size = ships[shipIndex][0];
            int count = ships[shipIndex][1];

            if (placedCount == count)
            {
                Solve(shipIndex + 1, 0, 0, 0);
                return;
            }

            for (int row = startRow; row < board.GetSize(); row++)
            {
                for (int col = row == startRow ? startCol : 0; col < board.GetSize(); col++)
                {
                    char[] directions = (size == 1) ? ['H'] : ['H', 'V'];
                    foreach (char direction in directions)
                    {
                        if (board.CanPlaceShip(row, col, size, direction))
                        {
                            board.PlaceShip(row, col, size, direction);
                            Solve(shipIndex, placedCount + 1, row, col);
                            board.RemoveShip(row, col, size, direction);
                        }
                    }
                }
            }
        }

        public List<string> GetUniqueSolutions() => [.. uniqueSolutions];
        public int GetSolutionsCount() => solutionsCount;
    }
}
