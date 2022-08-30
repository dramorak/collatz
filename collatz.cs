// program for calculating collatz sequences.

using System
using System.Collections.Generic

class Program
{
    public static void main()
    {
        public int CollatzStep(int n)
        {
            if(n % 2 == 1)
            {
                return 3 * n + 1;
            }
            else 
            {
                return n / 2;
            }
        }

        public int CollatzSequenceLength(int n)
        {
            l = 0;
            while(n != 1)
            {
                l += 1;
                n = CollatzStep(n);
            }
        }

        public void MonteCarlo(int start, int end, int number)
        {
            //takes random guesses at numbers between start and end.
        }
    }
}

class ReallyBigNum
{
    public List<
}