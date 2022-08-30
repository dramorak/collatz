import System.Win32 (COORD(x))

collatzStep :: Integer -> Integer
collatzStep 1 = 1
collatzStep n
   | mod n 2 == 1 = 3 * n + 1
   | otherwise    = div n 2 

collatzSequence :: Integer -> [Integer]
collatzSequence 1 = [1]
collatzSequence n = n : collatzSequence (collatzStep n)

intListLength :: [Integer] -> Integer
intListLength []     = 0
intListLength (x:xs) = 1 + intListLength xs 

collatzLength :: Integer -> (Integer, Integer)
collatzLength n = ((intListLength (collatzSequence n)) - 1, n)

mMax :: (Integer, Integer) -> (Integer, Integer) -> (Integer, Integer)
mMax (x,y) (z,w) 
    | x > z     = (x,y)
    | otherwise = (z,w)

findMaxLength :: Integer -> Integer -> Integer -> (Integer, Integer)
findMaxLength start end step
    | start > end = (0,0)
    | otherwise   = mMax (collatzLength start) (findMaxLength (start + step) end step)