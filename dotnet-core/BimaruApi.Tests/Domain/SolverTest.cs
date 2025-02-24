using BimaruApi.Domain;

namespace BimaruApi.Tests.Domain
{
    public class SolverTest
    {
        [Fact]
        public void TestSolve()
        {
            var sut = new Solver(new Board("""
                1 | . . .
                1 | . . .
                2 | v . .
                    2 0 2
                """));

            Assert.True(sut.Solve());
            
            List<string> solutions = sut.GetUniqueSolutions();
            Assert.Equal(1, sut.GetSolutionsCount());
            Assert.Single(solutions);
            Assert.Equal("""
                1 | ~ ~ o
                1 | ^ ~ ~
                2 | v ~ o
                    2 0 2
                """.NormalizeLineEndings(), solutions[0].NormalizeLineEndings());
        }
    }
}
