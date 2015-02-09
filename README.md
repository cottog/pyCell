# pyCell
My attempt at using elementary cellular automata to create a cryptographic hash function.

I did this for a class project, and it helped me get an 'A' without taking a terribly long amount of time at all. 

I thought elementary CAs were an interesting topic, and I saw a few research papers discussing how effectively they could possibly be used for that task, and I set out to prove how ineffectively I could use them for that task. 

The file test.py has a few tests that I thought might provide some useful information. I cannot possibly prove whether or not any cryptographic hash functions are effective, but the test file provides a few useful metrics: it proves that hashing the same string will always return the same hash, it looks for hash collisions within a very small set of randomly generated strings, and it looks at the difference (in percentage of bits flipped) between the hashes of two strings that differ by a single bit ( assuming the user plays along and inputs two such strings).


# License and Disclaimer
This code is free to be used and distributed however you wish, in whole or in part, so long as there is an attribution to "cottog" somewhere in the source of whatever project you use this code for. Or, if you'd like, a link to this repo. 

That being said, I make no claims as to the efficacy, efficiency, extensibility, elegance, synergy, or any other such attributes that could possibly be ascribed to this code. It is barely tested, and definitely unproven, so please don't use it for anything other than novelty. I do not believe it should be used for purposes of authentication or integrity checking or anything else. 

