max_samples           = 100        # maximum number of samples
adapt_samples         = 10         # interval of samples for adaption of p-value

# list of p_values used as supporting points for a generated polynomial
hitting_propability   = [0.1, 0.5, 0.6, 0.7, 0.9]
deg_p_polynomial      = 2          # degree of approximation polynomial
# list of step_values used as supporting points for a generated polynomial
step_width            = [0.9, 0.7, 0.6, 0.5, 0.1]
deg_s_polynomial      = 2          # degree of approximation polynomial
max_step              = 10         # maximum step size

show_polynomials      = False      # show approximation polynomials


max_pe = 16                        # number of processors
distr = "uniform"                  # distribution of samples (uniform, binomial)
shape = "cube"                     # shape of the used hypervolume (cube)
