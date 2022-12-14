// program for calculating collatz sequences.

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Numerics;
using System.Runtime;
class Program
{

    private static PrecomputationTables T = new PrecomputationTables(5); 
    public static int CollatzSequenceLengthImproved(int n)
    {
        //returns the stopping time of n. (the number of steps before n reaches 1).
        int length = 0;
        int mod = (int)(Math.Pow(2, 5) - 1);
        while(n > mod)
        {
            int a = n >> 5;
            int b = n & mod;
            n = T.C3[b] * a + T.D[b];
            length += 5 + T.C[b];
        }
        length += T.L[n];
        return length;
    }
    public static BigInteger CollatzStep(BigInteger n)
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

    public static BigInteger CollatzSequenceLength(BigInteger n)
    {
        int l = 0;
        while (n != 1)
        {
            if (n % 2 == 0)
            {
                n = n / 2;
                l += 1;
            }
            else
            {
                n = (3 * n + 1) / 2;
                l += 2;
            }
        }
        return l;
    }

    /// <summary>
    /// Makes numGuesses guesses between start, end,
    /// </summary>
    /// <param name="start"></param>
    /// <param name="end"></param>
    /// <param name="numGuesses"></param>
    /// <param name="outputFile"></param>
    public static int MonteCarlo(int[] c, int[] d, int[] c3, int[] l, int k, BigInteger numGuesses, string outputFile)
    {

        StreamWriter sw = File.AppendText(outputFile);
        BigInteger newNum, newNumCopy, a;
        int b;
        byte[] randomByteArray = new byte[43] { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 17, 0};
        var rand = new Random();
        int mod = (int)(Math.Pow(2, k) - 1);
        int length = 0;
        int count = 0;
        int max_found = 0;
        while (count < numGuesses)
        {
            //find random bigint
            rand.NextBytes(randomByteArray);
            randomByteArray[0] = 27;
            randomByteArray[41] = 17;
            randomByteArray[42] = 0;
            newNum = new BigInteger(randomByteArray);
            newNumCopy = newNum;

            //perfom k-step shortcut
            length = 0;
            while (newNumCopy > mod)
            {
                a = newNumCopy >> k;
                b = (int)(newNumCopy & mod);
                newNumCopy = c3[b] * a + d[b];
                length += k + c[b];
            }
            length += l[(int)newNumCopy];
            //check to see if a record has been made.
            if (length > max_found)
            {
                max_found = length;
                sw.WriteLine(max_found + " " + newNum);
            }
            count += 1;
        }

        //delete sw
        sw.WriteLine("\n\n");
        sw.Dispose();

        //return max_found
        return max_found;

    }

    public static void TestValues()
    {
        string path = @"C:\Users\dramo\programs\contest\collatz\csharp implementation\collatz\record2.txt";
        PrecomputationTables tables;
        double m = double.MaxValue;
        int k = 0;
        for(int j = 2; j < 20; j++)
        {
            tables = new PrecomputationTables(j);
            DateTime before = DateTime.Now;
            MonteCarlo(tables.C, tables.D, tables.C3, tables.L, j, 10000, path);
            DateTime after = DateTime.Now;
            Console.WriteLine($"Value tested:{j}\n\nTime elapsed: {(after - before).TotalSeconds}\n\n");
            
            if((after - before).TotalSeconds < m)
            {
                k = j;
                m = (after - before).TotalSeconds;
            }
            
        }
        Console.WriteLine($"\n\nBest found: k = {k}, with time {m}");
        Console.Read();
    }

    public static void RunMonteCarlo()
    {
        int calculations;
        int rate = 54000;
        bool doCalculation;
        do
        {
            Console.WriteLine("Please enter the number of large numbers you wish to check:");
            string? input = Console.ReadLine();
            doCalculation = int.TryParse(input, out calculations);
            if (!doCalculation)
            {
                Console.WriteLine("\tERROR:Couldn't parse input. Please enter another number.");
            }
            else
            {
                Console.WriteLine($"{calculations} numbers to be checked. This is estimated to take {(float)calculations / rate / 3600} hours. Is this okay?(y/n)");
                input = Console.ReadLine();
                if (input == null || !(input.ToLower() == "y" || input.ToLower() == "yes"))
                {
                    doCalculation = false;
                }
            }
        } while (!doCalculation);


        string path = @"C:\Users\dramo\programs\contest\collatz\csharp implementation\collatz\record.txt";

        //control variable
        int k = 17;

        //precompute values.
        Console.WriteLine("Constructing pre-computation tables...");
        PrecomputationTables tables = new PrecomputationTables(k);

        Console.WriteLine("Starting computations...");
        //timeit
        DateTime before = DateTime.Now;
        int maxFound = MonteCarlo(tables.C, tables.D, tables.C3, tables.L, k, calculations, path);
        DateTime after = DateTime.Now;
        Console.WriteLine($"Time elapsed: {(after - before).TotalSeconds}\n\n");
        Console.WriteLine($"Largest stopping time found: {maxFound}. Record can be found at {path}");
        Console.WriteLine("Press <enter> to exit.");
        Console.Read();
    }
    public static void Main()
    {
        RunMonteCarlo(); 
    }
}

class PrecomputationTables
{
    private int[] c, d, c3, l;

    public int[] C { get { return c; } }
    public int[] C3 { get { return c3; } }
    public int[] D { get { return d; } }
    public int[] L { get { return l; } }

    public PrecomputationTables(int k)
    {
        k = Math.Max(k, 1);
        int size = (int)Math.Pow(2, k);
        c = new int[size];
        d = new int[size];
        c3 = new int[size];
        l = new int[size];

        //c is the number of increases after k applications of (shortened) collatz step.
        //d is the result of applying f* to i k times.
        //c3 is the cube of c
        //l is the collatz sequence length of i.
        c3[0] = 1;
        for(int i = 1; i < size; i++)
        {
            int increases = 0;
            int n = i;
            for(int j = 0; j < k; j++)
            {
                if(n%2 == 0)
                {
                    n = n / 2;
                }
                else
                {
                    n = (3 * n + 1) / 2;
                    increases++;
                }
            }
            c[i] = increases;
            d[i] = n;
            c3[i] = (int)Math.Pow(3, c[i]);

            l[i] = (int)Program.CollatzSequenceLength(i);
        }
    }
}