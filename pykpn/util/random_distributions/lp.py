from scipy.stats import gengamma
import random
#Josefine Asmus, Christian L. Mueller and Ivo F. Sbalzarini. Lp-Adaptation: Simultaneous Design Centering and Robustness Estimation of Electronic and Biological Systems — Supplementary Information —
#Calafiore, G., Dabbene, F. & Tempo, R. Uniform sample generation in l p balls for probabilistic robustness analysis.
#def uniformFromLPBall():
def p_norm(x,p):
    res = sum(map(lambda t : t**p,x))
    return res**(1/p)
        
def uniform_from_p_ball(p=1,n=2):
    a, c = 1/p, p
    #1. Sample n real scalars i.i.d. from the generalized Gamma distribution ξi ∼ G ̃ ( 1 , p). p
    r = gengamma.rvs(a, c, size=n)
    signs = random.choices([1,-1],k=n)
    #2. Construct a vector x ∈ Rn with components xi = siξi, where si are independent uniformly random signs.
    vec = r*signs
    #3. Compute z = w1/n, where w is a random variable uniformly distributed in the interval [0,1]. 
    z = random.random()**n
    y = z * 1/p_norm(vec,p)* vec
    #4. Return y = z x , where ∥x∥p = (∑n |xi|p)1/p.
    return y

x = []
y = []
for i in range(1000):
    vec = uniform_from_p_ball(p=1,n=2)
    x.append(vec[0])
    y.append(vec[1])
    

import matplotlib.pyplot as plt

plt.scatter(x,y)
plt.show()
