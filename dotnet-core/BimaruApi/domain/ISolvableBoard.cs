namespace BimaruApi.Domain
{
    public interface ISolvableBoard
    {
        void ResetBoard();
        bool CanPlaceShip(int row, int col, int size, char direction);
        void PlaceShip(int row, int col, int size, char direction);
        void RemoveShip(int row, int col, int size, char direction);
        bool IsValidSolution();
        int GetSize();
        string AsText { get; }
    }
}
