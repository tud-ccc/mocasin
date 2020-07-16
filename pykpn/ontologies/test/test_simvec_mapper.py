#Copyright (C) 2019-2020 TU Dresden
#All Rights Reserved
#
#Authors: Felix Teweleit, Andrés Goens

def testMappingGeneration1(solver):
    input_query = "EXISTS src MAPPED ARM00 AND fft_l MAPPED ARM01"
    result = solver.request(input_query)
    assert result.affinity(result.kpn.find_process('src')).name == 'ARM00'
    assert result.affinity(result.kpn.find_process('fft_l')).name == 'ARM01'

def testMappingGeneration2(solver):
    input_query = "EXISTS src MAPPED ARM00 AND fft_l MAPPED ARM01 AND sink MAPPED ARM02"
    result = solver.request(input_query)
    assert result.affinity(result.kpn.find_process('src')).name == 'ARM00'
    assert result.affinity(result.kpn.find_process('fft_l')).name == 'ARM01'
    assert result.affinity(result.kpn.find_process('sink')).name == 'ARM02'

def testMappingGeneration3(solver):
    input_query = "EXISTS filter_l MAPPED ARM03 AND fft_l MAPPED ARM04 AND RUNNING TOGETHER [src, filter_l ]"
    result = solver.request(input_query)

    assert result.affinity(result.kpn.find_process('src')).name == 'ARM03'
    assert result.affinity(result.kpn.find_process('filter_l')).name == 'ARM03'
    assert result.affinity(result.kpn.find_process('fft_l')).name == 'ARM04'


def testMappingGeneration4(solver):
    input_query = "EXISTS src MAPPED ARM03 AND ARM05 PROCESSING AND ARM06 PROCESSING"
    result = solver.request(input_query)
    assert result.affinity(result.kpn.find_process('src')).name == 'ARM03'
    result = result.to_list()
    assert(result.count(5) >= 1)
    assert(result.count(6) >= 1)

def testMappingGeneration5(map_dict_solver):
    input_query = "EXISTS RUNNING TOGETHER [src, fft_l, fft_r, filter_l, filter_r, ifft_l, ifft_r, sink ]" \
                  "AND EQUALS map_two"
    result = map_dict_solver.request(input_query).to_list()
    assert(result.count(result[0]) == 8)

def testMappingGeneration6(map_dict_solver):
    input_query = "EXISTS RUNNING TOGETHER [src, sink ] AND EQUALS map_one"
    assert not map_dict_solver.request(input_query)
    
def testMappingGeneration7(map_dict_solver):
    input_query = "EXISTS src MAPPED ARM00 AND filter_l MAPPED ARM01 AND RUNNING TOGETHER [src, filter_l ]"
    assert not map_dict_solver.request(input_query)

def testSetVector1(solver):
    input_query = "EXISTS src MAPPED ARM00 AND fft_l MAPPED ARM01"
    state_vec = [4, 5, 1, 2, 0, 0]
    result = solver.request(input_query, vec=state_vec)
    assert result.affinity(result.kpn.find_process('src')).name == 'ARM00'
    assert result.affinity(result.kpn.find_process('fft_l')).name == 'ARM01'

def testSetVector2(solver):
    input_query = "EXISTS src MAPPED ARM00 AND fft_l MAPPED ARM01 AND sink MAPPED ARM02"
    state_vec = [1, 1, 1, 1, 1]
    result = solver.request(input_query, vec=state_vec)
    assert result.affinity(result.kpn.find_process('src')).name == 'ARM00'
    assert result.affinity(result.kpn.find_process('fft_l')).name == 'ARM01'
    assert result.affinity(result.kpn.find_process('sink')).name == 'ARM02'

def testSetVector3(map_dict_solver):
    input_query = "EXISTS RUNNING TOGETHER [src, fft_l, fft_r, filter_l, filter_r, ifft_l, ifft_r, sink ] AND EQUALS" \
                  "map_two"
    state_vec = ["some nonsense"]
    result = map_dict_solver.request(input_query, vec=state_vec).to_list()
    assert(result.count(result[0]) == 8)
