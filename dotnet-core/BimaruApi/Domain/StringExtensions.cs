namespace BimaruApi.Domain
{
    public static class StringExtensions
    {
        public static string NormalizeLineEndings(this string input)
        {
            return input.Replace("\r\n", "\n").Replace("\r", "\n");
        }
    }
}
