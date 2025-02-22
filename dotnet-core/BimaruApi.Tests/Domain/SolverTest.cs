using BimaruApi.Domain;

namespace BimaruApi.Tests.Domain
{
    public class SolverTest
    {
        [Fact]
        public void TestSolve()
        {
            var sut = new Solver(new Board("""
                6 | . . . . . . . . ~ .
                0 | . . . . . . . . . .
                1 | . . . . . . . . . .
                0 | . . . . . . . . . .
                2 | . . . . . . . . . .
                3 | . . . . . . . . < .
                0 | . . . . . . . . . .
                2 | . . . . . . . . . .
                3 | . ~ . . . . . . . .
                3 | . . . . . . . . . .
                    3 4 1 4 2 0 1 0 3 2
                """));

            Assert.True(sut.Solve());
            
            List<string> solutions = sut.GetUniqueSolutions();
            Assert.Equal(1, sut.GetSolutionsCount());
            Assert.Single(solutions);
            Assert.Equal("""
                6 | ~ < □ □ > ~ o ~ ~ o
                0 | ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
                1 | ~ o ~ ~ ~ ~ ~ ~ ~ ~
                0 | ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
                2 | ~ ^ ~ ~ o ~ ~ ~ ~ ~
                3 | ~ v ~ ~ ~ ~ ~ ~ < >
                0 | ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
                2 | ^ ~ ~ ^ ~ ~ ~ ~ ~ ~
                3 | □ ~ ~ □ ~ ~ ~ ~ ^ ~
                3 | v ~ ~ v ~ ~ ~ ~ v ~
                    3 4 1 4 2 0 1 0 3 2
                """.NormalizeLineEndings(), solutions[0].NormalizeLineEndings());
        }
    }
}
