import dc_sample

class Oracle(object):
     def __init__(self):
         type(self).test_set = TestSet()

     
     def validate(self, sample):
         return type(self).test_set.test_oracle(sample.sample2tuple())


# This is a temporary test class
class TestSet(object):
     # specify a fesability test set
     def test_oracle(self, s):
         """ test oracle function (2-dim) """
         if (len(s) != 2):
             print("test oracle requires a dimension of 2\n")
             return 0
         x = s[0]
         y = s[1]
         if ((x in range(1,3)) and (y in range(1,3))): # 1<=x<=2 1<=y<=2
             return 1
         if ((x in range(7,13)) and (y in range(7,13))): # 1<=x<=5 1<=y<=5
             return 1
         else:
             return 0

