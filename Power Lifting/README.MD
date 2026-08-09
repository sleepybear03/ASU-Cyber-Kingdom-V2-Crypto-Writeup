in this challenge, we are essentially provided the following equations:

out1=(p+5q)power1;(mod;n)

out2=(2p−3q)power2;(mod;n)

Where p and q are the primes whose product is n. We of course need to find these in order to break the RSA encryption, whose ciphertext is c.

Notably, however, we are not provided out1 in our output file! Instead, we are provided 'hint' , which is the smallest prime after eq1. Well, before figuring out if we can solve this problem without out1 specifically, let's first solve the case where we are given out1. How can we do this?
First, I'll rewrite the variables to make it a little easier to read.

o1=(p+5q)p1;(mod;n)

o2=(2p−3q)p2;(mod;n)

Let's now take our equations, and raise each of them to the other's power, i.e.:

op21=(p+5q)p1p2;(mod;n)

op12=(2p−3q)p2p1;(mod;n)

Because of Binomial Theorem, we know this will simplify to:

op21=(p)p1p2+(5q)p1p2;(mod;n)

op12=(2p)p2p1+(−3q)p1p2;(mod;n)

Since all other terms have a pq, which is equal to n, in them.

Let's now take both equations (mod q). Then, the q's will essentially cease to exist in our equations. Note that the (mod n) does not affect this because q is a factor of n.

op21=(p)p1p2;(mod;q)

op12=(2p)p2p1;(mod;q)

Now, what if we do this:

op21⋅2p1p2=(p)p1p2⋅2p1p2;(mod;q)

op12=(2p)p2p1;(mod;q)

Therefore:

op21⋅2p1p2=(2p)p1p2;(mod;q)

op12=(2p)p2p1;(mod;q)

Based on the definition of modular arithmetic, we can then write:

op21⋅2p1p2=(2p)p1p2+k1q

op12=(2p)p2p1+k2q

And thus,

x=op21⋅2p1p2−op12=(2p)p1p2+k1q−((2p)p2p1+k2q)=(k1−k2)q

Hence, we have now produced a number that is a multiple of q. And thus gcd(x, n) will return q.

Perfect. So now we know how to factor n if we did know out_1. But unfortunately, we don't. We only the know the smallest prime greater than it. So how we can do this?

I immediately thought of brute forcing out_1 by just sequentially checking numbers less than eq1 until we find an out_1 that works.
