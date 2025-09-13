namespace BimaruApi.Domain
{
    public class Board : ISolvableBoard
    {
        protected readonly int size;
        protected readonly char[,] grid;
        protected readonly int[] rowConstraints;
        protected readonly int[] colConstraints;
        protected readonly List<Cell> initialCells;

        public Board(string puzzle) : this(puzzle, 10) { }

        protected Board(string puzzle, int size)
        {
            this.size = size;
            grid = new char[this.size, this.size];
            rowConstraints = new int[this.size];
            colConstraints = new int[this.size];
            initialCells = new List<Cell>();
            ParseInput(puzzle);
        }

        private void ParseInput(string puzzle)
        {
            var lines = puzzle.NormalizeLineEndings().Split('\n');
            for (int i = 0; i < size; i++)
            {
                var parts = lines[i].Split('|');
                rowConstraints[i] = int.Parse(parts[0].Trim());
                var rowValues = parts[1].Trim().Split(' ');
                for (int j = 0; j < size; j++)
                {
                    grid[i, j] = rowValues[j][0];
                    if (grid[i, j] != '.')
                    {
                        initialCells.Add(new Cell(i, j, grid[i, j]));
                    }
                }
            }
            var colValues = lines[size].Trim().Split(' ');
            for (int j = 0; j < size; j++)
            {
                colConstraints[j] = int.Parse(colValues[j]);
            }
        }

        public void ResetBoard()
        {
            for (int i = 0; i < size; i++)
            {
                for (int j = 0; j < size; j++)
                {
                    grid[i, j] = '.';
                }
            }
        }

        public bool CanPlaceShip(int row, int col, int size, char direction)
        {
            if (direction != 'H' && direction != 'V') return false;
            bool isHorizontal = direction == 'H';

            int maxIndex = isHorizontal ? col + size : row + size;
            if (maxIndex > this.size) return false;

            int[] constraints = isHorizontal ? rowConstraints : colConstraints;
            int num = isHorizontal ? row : col;

            if (constraints[num] - CountShipCells(num, isHorizontal) < size) return false;

            int[] opposingConstraints = isHorizontal ? colConstraints : rowConstraints;
            for (int i = 0; i < size; i++)
            {
                int r = isHorizontal ? row : row + i;
                int c = isHorizontal ? col + i : col;

                if (r >= this.size || c >= this.size || grid[r, c] != '.') return false;

                int index = isHorizontal ? col + i : row + i;
                if (opposingConstraints[index] - CountShipCells(index, !isHorizontal) < 1) return false;

                for (int dr = -1; dr <= 1; dr++)
                {
                    for (int dc = -1; dc <= 1; dc++)
                    {
                        int nr = r + dr;
                        int nc = c + dc;
                        if (nr >= 0 && nr < this.size && nc >= 0 && nc < this.size)
                        {
                            if (grid[nr, nc] != '.' && grid[nr, nc] != '~') return false;
                        }
                    }
                }
            }

            return true;
        }

        private int CountShipCells(int index, bool isRow)
        {
            int count = 0;
            for (int i = 0; i < size; i++)
            {
                char cell = isRow ? grid[index, i] : grid[i, index];
                if (cell != '.' && cell != '~') count++;
            }
            return count;
        }

        private static string GetShipRepresentation(int size, char direction) {
            if (size == 1) return "o"; // Kein Austausch nötig!

            string middle = new('□', Math.Max(0, size - 2));
            string ship = '<' + middle + '>';

            return (direction == 'H') ? ship : ship.Replace('<', '^').Replace('>', 'v');
        }

        public void PlaceShip(int row, int col, int size, char direction)
        {
            if (!CanPlaceShip(row, col, size, direction)) return;
            string representation = GetShipRepresentation(size, direction);
            for (int i = 0; i < size; i++)
            {
                int r = row + (direction == 'V' ? i : 0);
                int c = col + (direction == 'H' ? i : 0);
                grid[r, c] = representation[i];
            }
        }

        public void RemoveShip(int row, int col, int size, char direction)
        {
            for (int i = 0; i < size; i++)
            {
                int r = direction == 'H' ? row : row + i;
                int c = direction == 'H' ? col + i : col;
                grid[r, c] = '.';
            }
        }

        public bool IsValidSolution()
        {
            foreach (Cell cell in initialCells) {
                char valueGrid = grid[cell.Row, cell.Col];
                char valueCell = cell.Value == '~'
                    ? '.' // Behandle Wasser wie leere Zelle
                    : cell.Value;
                if (valueGrid != valueCell)
                    return false;
            }
            return true;
        }

        public int GetSize() => size;

        public string AsText => ToString().Replace(".", "~");

        public override string ToString()
        {
            var rows = Enumerable
                .Range(0, rowConstraints.Length)
                .Select(i => $"{rowConstraints[i]} | {string.Join(" ", GetRow(i))}");

            var lastRow = "    " + string.Join(" ", colConstraints.Select(c => c.ToString()));

            return string.Join("\n", rows) + "\n" + lastRow;
        }

        private char[] GetRow(int rowIndex)
        {
            return [.. Enumerable
                .Range(0, colConstraints.Length)
                .Select(j => grid[rowIndex, j])];
        }
    }
}
