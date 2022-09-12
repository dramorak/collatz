Result of me trying to do the "Collatz Sequence" challenge on topcoder. (https://www.topcoder.com/challenges/3523079f-8df9-4731-9dbc-d8ded0660992?tab=details)

The Collatz Conjecture is the simplest unsolved question in mathematics. It goes as follows:

For each integer Z > 0, define f:Z -> Z to be the following:
	f(n) = n / 2 if n is even
	f(n) = 3*n + 1 if n is odd
Does this sequence reach "1" eventually for every positive integer?

The challenge featured trying to find numbers with especially long collatz seuquences. I tried 2 approaches: First, I guessed 3 billion numbers randomly, trying to find 
the longest collatz-sequence numbers I could find. Secondly, I tried working the opposite way, exploring the tree built using the inverse operation:
	g(n) = {2n, or (n-1)/3 if n % 6 == 4}

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
The results:
	Best found through first method: 
		9922476685051589024883668549160616536581172988589061013662629929232031622326871748015254089443296987
	with length:
		4489

	/////
	Best found through second method:
		9242551121369642493177480095113700596467139696844140161787842563116745806405541671252722951876262683
	with length:
		10331

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
As you can see, the second method turned out much better. I settled on a beam search algorithm. It's application to large search spaces is truly impressive,
it could be used almost everywhere. 
