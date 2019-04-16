import coverage
import unittest
import pykpn.test.test_permutations
import pykpn.test.test_metric_spaces
import pykpn.test.test_embeddings


if __name__ == "__main__":
    cov = coverage.Coverage()
    cov.start()
    
    suite = unittest.TestLoader().loadTestsFromModule(pykpn.test.test_permutations)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    suite = unittest.TestLoader().loadTestsFromModule(pykpn.test.test_metric_spaces)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    suite = unittest.TestLoader().loadTestsFromModule(pykpn.test.test_embeddings)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    cov.stop()
    cov.save()
    cov.report()