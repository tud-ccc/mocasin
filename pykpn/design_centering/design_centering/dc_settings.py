num_iterations        = 5              # maximum number of iterations
adapt_samples         = 10             # lambda: interval of samples for adaption of p-value
max_samples           = adapt_samples * num_iterations

# list of p_values used as supporting points for a generated polynomial
hitting_propability   = [0.1, 0.5, 0.6, 0.7, 0.9]
deg_p_polynomial      = 2              # degree of approximation polynomial
# list of step_values used as supporting points for a generated polynomial
step_width            = [0.9, 0.7, 0.6, 0.5, 0.1]
deg_s_polynomial      = 2              # degree of approximation polynomial
max_step              = 10             # maximum step size

show_polynomials      = False          # show approximation polynomials
show_points           = True           # show hit and miss points
visualize_mappings    = False


max_pe                = 16             # number of processors (for presentation only)
distr                 = "uniform"      # distribution of samples (uniform, binomial)
shape                 = "cube"         # shape of the used hypervolume (cube)
oracle                = "simulation"   # test set to use
#space_type           = "geom"         # Type of design space (geom, metric) #deprecated!

random_seed           = 42             # Initialization for the RNG (None means random init)
threshold             = 280            # Threshold for feasibility

run_perturbation      = True           # Run Perturbation Tests
num_perturbations     = 10             # Number of perturbations per mapping
num_mappings          = 10             # Number of random mappings to compare with

adaptable_center_weights = False
