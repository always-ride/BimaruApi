using BimaruApi.Domain;

namespace BimaruApi.Tests.Domain
{
    public class BoardTest
    {
        [Fact]
        public void TestParseInput()
        {
            var sut = new TestableBoard("""
                4 | . . . .
                0 | . . . .
                2 | . . . .
                0 | . . . .
                    1 2 1 2
                """);

            Assert.Equal([4, 0, 2, 0], sut.GetRowConstraints());
            Assert.Equal([1, 2, 1, 2], sut.GetColConstraints());
        }

        [Theory]
        [InlineData(0, 1, 1, 'H', true)]
        [InlineData(0, 1, 3, 'H', true)]
        [InlineData(1, 0, 1, 'H', false)]
        [InlineData(2, 1, 1, 'H', false)]
        [InlineData(2, 0, 1, 'H', true)]
        [InlineData(2, 0, 1, 'V', true)]
        public void TestCanPlaceShip(int row, int col, int length, char direction, bool expected)
        {
            var sut = new TestableBoard(SIMPLE_BOARD);
            Assert.Equal(expected, sut.CanPlaceShip(row, col, length, direction));
        }

        [Theory]
        [InlineData(0, 1, 3, 'H', "3 | . < □ >")]
        [InlineData(2, 0, 1, 'V', "3 | o . < >")]
        public void TestPlaceShip(int row, int col, int length, char direction, string expected)
        {
            var sut = new TestableBoard(SIMPLE_BOARD);
            sut.PlaceShip(row, col, length, direction);
            Assert.Equal(expected, sut.GetLine(row, 'H').Replace("^", "<").Replace("v", ">"));
        }

        private static readonly string SIMPLE_BOARD = """
            3 | . . . .
            0 | . . . .
            3 | . . < >
            0 | . . . .
                1 1 2 2
            """;

        class TestableBoard(string puzzle) : Board(puzzle)
        {
            public int[] GetRowConstraints() => rowConstraints;
            public int[] GetColConstraints() => colConstraints;

            public string GetLine(int index, char direction)
            {
                int constraint = direction == 'H' ? rowConstraints[index] : colConstraints[index];
                var line = new System.Text.StringBuilder($"{constraint} |");
                for (int j = 0; j < size; j++)
                {
                    line.Append($" {(direction == 'H' ? grid[index, j] : grid[j, index])}");
                }
                return line.ToString();
            }
        }
    }
}
