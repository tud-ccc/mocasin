from . import dc_sample
from . import dc_settings as conf

from sys import exit

class Oracle(object):
     def __init__(self):
          if conf.oracle == "TestSet":
               type(self).test_set = TestSet()
          elif conf.oracle == "TestTwoPrKPN":
               type(self).test_set = TestTwoPrKPN()
          else:
               print("Error, unknown oracle:" + conf.oracle)
               exit(1)


     def validate(self, sample):
               res =  type(self).test_set.oracle(sample.sample2tuple())
               #print("oracle for: " + str(sample.sample2tuple()) + ", " + str(res))
               return res

# This is a temporary test class
class TestSet(object):
     # specify a fesability test set
     def oracle(self, s):
         """ test oracle function (2-dim) """
         #print("oracle for: " + str(s))
         if (len(s) != 2):
             print("test oracle requires a dimension of 2\n")
             exit(1)
         x = s[0]
         y = s[1]
         if ((x in range(1,3)) and (y in range(1,3))): # 1<=x<=2 1<=y<=2
             return True
         if ((x in range(1,4)) and (y in range(13,15))):
             return True
         if ((x in range(9,11)) and (y in range(9,11))):
             return False
         if ((x in range(7,13)) and (y in range(7,13))):
             return True
         else:
             return False


class TestTwoPrKPN():
     def oracle(self,s):
          """ test oracle function (2-dim) """
          if (len(s) != 2):
               print("test oracle requires a dimension of 2\n")
               exit(1)
          x = s[0]
          y = s[1]
          if x == y: #same PE
               return False
          elif x < 0 or x > 15 or y < 0 or y > 15: #outside of area
               #print("outside area")
               return False
          elif divmod(x,4)[0] == divmod(y,4)[0]: # same cluster
               return True
          else:
               return False

