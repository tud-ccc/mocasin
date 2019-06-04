# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from pykpn.gui.utils import listOperations as lo
from pykpn.gui.utils import platformOperations as po

class TestListOperations(object):

    def test_convertToMatrix_1(self):
        testList = [1,2,3,4,5,6,7,8,9]
        result = [[1,2,3], [4,5,6], [7,8,9]]
        assert(lo.convertToMatrix(testList) == result)
    
    def test_convertToMatrix_2(self):
        testList = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
        result = [[1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16]]
        assert(lo.convertToMatrix(testList) == result)
    
    def test_convertToMatrix_3(self):
        testList = [1,2,3,4,5,6,7]
        result = [[1,2,3], [4,5,6], [7]]
        assert(lo.convertToMatrix(testList) == result)
    
    def test_convertToMatrix_4(self):
        testList = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
        result = [[1,2,3,4,5], [6,7,8,9,10], [11,12,13,14,15], [16,17,18,19]]
        assert(lo.convertToMatrix(testList) == result)
    
    def test_getDimension_1(self):
        testMatrix = [[1,2,3,4,5], [6,7,8,9,10], [11,12,13,14,15], [16,17,18,19]]
        assert(lo.getDimension(testMatrix) == 5)
        
    def test_getDimension_2(self):
        testMatrix = [[1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16]]
        assert(lo.getDimension(testMatrix) == 4)
    
    def test_getDimension_3(self):
        testMatrix = [1]
        assert(lo.getDimension(testMatrix) == 1)
    
    def test_getDimension_4(self):
        testMatrix = 1
        assert(lo.getDimension(testMatrix) == 1)
    
    def test_containsItem_1(self):
        testList = [1,2,3,4,5]
        assert(lo.containsItem(testList, 5))
    
    def test_containsItem_2(self):
        testList = (1,2)
        assert(lo.containsItem(testList, 2))
    
    def test_containsItem_3(self):
        testList = [[1,2,[2,3,4]],[9],[23],(1,[9])]
        assert(lo.containsItem(testList, 3))

    def test_containsItem_4(self):
        testList = [[1,2,[2,3,4]],[9],[23],(1,[9])]
        assert(lo.containsItem(testList, 9))

    def test_containsItem_5(self):
        testList = [[1,2,[2,3,4]],[9],[23],(1,[9])]
        assert(not lo.containsItem(testList, 34))

class TestPlatformOperations(object):
    
    def test_peToString_1(self, exynos):
        result = po.peToString(exynos.processors())
        assert(result == ['ARM00','ARM01','ARM02','ARM03','ARM04','ARM05','ARM06','ARM07'])
    
    def test_peToString_2(self, parallella):
        result = po.peToString(parallella.processors())
        assert(result == ['ARM0', 'ARM1', 'E00', 'E01', 'E02', 'E03', 'E04', 'E05', 'E06',
                          'E07', 'E08', 'E09', 'E10', 'E11', 'E12', 'E13', 'E14', 'E15'])
    
    def test_peToString_3(self, multiDSP):
        result = po.peToString(multiDSP.processors())
        assert(result == ['dsp0', 'dsp1', 'dsp2', 'dsp3', 'dsp4'])
    
    def test_getSortedProcessorScheme_1(self, exynos):
        result = po.peToString(exynos.processors())
        result = po.getSortedProcessorScheme(result)
        assert(result == ['ARM00','ARM01','ARM02','ARM03','ARM04','ARM05','ARM06','ARM07'])
        
    def test_getSortedProcessorScheme_2(self, parallella):
        result = po.peToString(parallella.processors())
        result = po.getSortedProcessorScheme(result)
        assert(result == ['ARM0', 'E00', 'ARM1', 'E01', 'E02', 'E03', 'E04', 'E05', 'E06',
                          'E07', 'E08', 'E09', 'E10', 'E11', 'E12', 'E13', 'E14', 'E15'])
        
    def test_getSortedProcessorScheme_3(self, multiDSP):
        result = po.peToString(multiDSP.processors())
        result = po.getSortedProcessorScheme(result)
        assert(result == ['dsp0', 'dsp1', 'dsp2', 'dsp3', 'dsp4'])
        
    def test_getMembersOfPrimitive_1(self, exynos):
        primitive = exynos.find_primitive('comm_DRAM')
        result = po.getMembersOfPrimitive(primitive)
        assert(result == ['ARM00','ARM01','ARM02','ARM03','ARM04','ARM05','ARM06','ARM07'])
        
    def test_getMembersOfPrimitive_2(self, parallella):
        primitive = parallella.find_primitive('EMEM')
        result = po.getMembersOfPrimitive(primitive)
        assert(result == ['ARM0', 'ARM1', 'E00', 'E01', 'E02', 'E03', 'E04', 'E05', 'E06',
                          'E07', 'E08', 'E09', 'E10', 'E11', 'E12', 'E13', 'E14', 'E15'])
        
    def test_getMembersOfPrimitive_3(self, multiDSP):
        primitive = multiDSP.find_primitive('comm_cp_shared_shared_memory')
        result = po.getMembersOfPrimitive(primitive)
        assert(result == ['dsp0', 'dsp1', 'dsp2', 'dsp3', 'dsp4'])
        








