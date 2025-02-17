namespace BimaruApi.Domain
{
    public class Cell
    {
        public int Row { get; }
        public int Col { get; }
        public char Value { get; }

        public Cell(int row, int col, char value)
        {
            Row = row;
            Col = col;
            Value = value;
        }

        public override string ToString()
        {
            return $"{Value}({Row},{Col})";
        }
    }
}
