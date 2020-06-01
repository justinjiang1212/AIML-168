import matplotlib.pyplot as plt
import numpy as np
import pymc3
import scipy.stats as stats

plt.style.use("ggplot")


n = 50 
z = 10 
alpha = 12 
beta = 12 
alpha_post = 22 
beta_post = 52

iterations = 100000

basic_model = pymc3.Model()

with basic_model:
    theta = pymc3.Beta("theta", alpha=alpha, beta=beta)
    
    y = pymc3.Binomial("y", n=n, p=theta, observed=z)
    
    start = pymc3.find_MAP()
    
    step = pymc3.Metropolis()
    
    trace = pymc3.sample(iterations, step, start, random_seed = 1, progressbar = True)
    

bins=50 
plt.hist(trace["theta"], bins, histtype="step", normed=True, label="Posterior (MCMC)", color="red")


x = np.linspace(0,1,100)
plt.plot(x, stats.beta.pdf(x, alpha, beta), "--", label = "Prior", color="blue")

plt.plot(x, stats.beta.pdf(x, alpha_post, beta_post), label= 'Posterior (Analytic)', color = "green")


plt.legend(title="Parameters", loc="best") 
plt.xlabel("$\\theta$, Fairness") 
plt.ylabel("Density") 
plt.show()

pymc3.traceplot(trace) 
plt.show()


import numpy as np
import matplotlib.pyplot as plt
from pymc3 import Model, Normal, HalfNormal, find_MAP, NUTS, sample, traceplot
from scipy import optimize
import pandas as pd
from pymc3 import Exponential, StudentT, Deterministic
from pymc3.distributions.timeseries import GaussianRandomWalk
from pymc3 import DiscreteUniform, Poisson


np.random.seed(123)

alpha, sigma = 1,1

beta = [1, 2.5]

size = 100

X1 = np.linspace(0, 1, size)
X2 = np.linspace(0, 0.2, size)

Y = alpha + beta[0]*X1 + beta[1]*X2 + np.random.randn(size)*sigma
basic_model = Model()
with basic_model:

    # Priors for unknown model parameters
    alpha = Normal('alpha', mu=0, sd=10)
    beta = Normal('beta', mu=0, sd=10, shape=2)
    sigma = HalfNormal('sigma', sd=1)

    # Expected value of outcome
    mu = alpha + beta[0]*X1 + beta[1]*X2

    # Likelihood (sampling distribution) of observations
    Y_obs = Normal('Y_obs', mu=mu, sd=sigma, observed=Y)

map_estimate = find_MAP(model=basic_model, method = "powell")
print(map_estimate)

with basic_model:
    start = find_MAP(method = "powell")
    step = NUTS(scaling=start)
    trace = sample(2000, step, start = start)

#traceplot(trace)
#the data that is installed with the package is not there
#returns = pd.read_csv('data/SP500.csv', index_col=0, parse_dates=True)



disaster_data = np.ma.masked_values([4, 5, 4, 0, 1, 4, 3, 4, 0, 6, 3, 3, 4, 0, 2, 6,
                            3, 3, 5, 4, 5, 3, 1, 4, 4, 1, 5, 5, 3, 4, 2, 5,
                            2, 2, 3, 4, 2, 1, 3, -999, 2, 1, 1, 1, 1, 3, 0, 0,
                            1, 0, 1, 1, 0, 0, 3, 1, 0, 3, 2, 2, 0, 1, 1, 1,
                            0, 1, 0, 1, 0, 0, 0, 2, 1, 0, 0, 0, 1, 1, 0, 2,
                            3, 3, 1, -999, 2, 1, 1, 1, 1, 2, 4, 2, 0, 0, 1, 4,
                            0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1], value=-999)
year = np.arange(1851, 1962)
##code is not working, for some reason
'''plot(year, disaster_data, 'o', markersize=8);
ylabel("Disaster count")
xlabel("Year")'''