max_samples          = 100       # maximum number of samples
adapt_samples        = 10        # interval of samples for adaption of p-value

# list of p_values used as supporting points for a generated approximation polynom
hitting_propability  = [0.1, 0.5, 0.6, 0.7, 0.9] 
deg_approx_polynom   = 2         # degree of approximation polynom
show_polynom         = False     # show approximation polynom  

max_pe = 16                      # number of processors
distr = "uniform"                # distribution of samples (uniform, binomial)
shape = "cube"                   # shape of the used hypervolume (cube)
