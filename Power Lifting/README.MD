In this challenge, we are essentially provided the following equations:
$$\text{out}_1 = (p + 5q)^{\text{power}_1} \pmod n$$
$$\text{out}_2 = (2p - 3q)^{\text{power}_2} \pmod n$$
Where $p$ and $q$ are the primes whose product is $n$. 
We of course need to find these in order to break the RSA encryption, whose ciphertext is $ciphertext$.Notably, however, we are not provided $\text{out}_1$ in our output file!
Instead, we are provided hint, which is the smallest prime after $\text{out}_1$.Well, before figuring out if we can solve this problem without $\text{out}_1$ specifically, let's first solve the case where we are given $\text{out}_1$. How can we do this?
First, I'll rewrite the variables to make it a little easier to read:
$$o_1 = (p + 5q)^{p_1} \pmod n$$
$$o_2 = (2p - 3q)^{p_2} \pmod n$$
Let's now take our equations, and raise each of them to the other's power, i.e.:
$$o_1^{p_2} = (p + 5q)^{p_1 p_2} \pmod n$$
$$o_2^{p_1} = (2p - 3q)^{p_2 p_1} \pmod n$$
Because of the Binomial Theorem, we know this will simplify to:
$$o_1^{p_2} = p^{p_1 p_2} + (5q)^{p_1 p_2} \pmod n$$
$$o_2^{p_1} = (2p)^{p_2 p_1} + (-3q)^{p_1 p_2} \pmod n$$
Since all other terms have a $pq$, which is equal to $n$, in them.
Let's now take both equations $\pmod q$. Then, the $q$'s will essentially cease to exist in our equations. Note that the $\pmod n$ does not affect this because $q$ is a factor of $n$.
$$o_1^{p_2} = p^{p_1 p_2} \pmod q$$
$$o_2^{p_1} = (2p)^{p_2 p_1} \pmod q$$
Now, what if we do this:$$o_1^{p_2} \cdot 2^{p_1 p_2} = p^{p_1 p_2} \cdot 2^{p_1 p_2} \pmod q$$
$$o_2^{p_1} = (2p)^{p_2 p_1} \pmod q$$
Therefore:$$o_1^{p_2} \cdot 2^{p_1 p_2} = (2p)^{p_1 p_2} \pmod q$$
$$o_2^{p_1} = (2p)^{p_2 p_1} \pmod q$$
Based on the definition of modular arithmetic, we can then write:
$$o_1^{p_2} \cdot 2^{p_1 p_2} = (2p)^{p_1 p_2} + k_1 q$$
$$o_2^{p_1} = (2p)^{p_2 p_1} + k_2 q$$
And thus,
$$x = o_1^{p_2} \cdot 2^{p_1 p_2} - o_2^{p_1} = (2p)^{p_1 p_2} + k_1 q - \left((2p)^{p_2 p_1} + k_2 q\right) = (k_1 - k_2) q$$
Hence, we have now produced a number that is a multiple of $q$. And thus $\gcd(x, n)$ will return $q$.Perfect. So now we know how to factor $n$ if we did know $\text{out}_1$. But unfortunately, we don't. We only know the smallest prime greater than it. So how can we do this?I immediately thought of brute forcing $\text{out}_1$ by just sequentially checking numbers less than hint until we find an $\text{out}_1$ that works.
After this, once we have q, we can simply do standard RSA procedure and decrypt the message. 
