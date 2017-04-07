import dc_sample

class Oracle(object):
     def __init__(self):
         print("create Oracle")
         type(self).test_set = TestSet()

     
     def validate(self, sample):
         print("oracle validate")
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
         if ((x in range(1,5)) and (y in range(1,6))): # 1<=x<=4 1<=y<=5
             return 1
         else:
             return 0

