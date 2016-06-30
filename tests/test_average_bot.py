from average_bot import *
import random
import string
import copy
import pytest

USERS_NUM = 6
STRING_LEN = 6

@pytest.fixture
def sums():
    sums1 = {}
    for i in xrange(0, USERS_NUM):
        rand_user = ''.join(random.choice(string.ascii_letters) for _ in range(STRING_LEN))
        sums1[rand_user] = {}
        sums1[rand_user]['sum'] = random.uniform(-1.0, 100.1)
        sums1[rand_user]['count'] = random.uniform(0, 9)
    return sums1

def test_is_float():
    assert is_float(random.uniform(-1.0, 2.9)) and \
           is_float(str(random.uniform(-1.0, 2.9)))

def test_is_float_false():
    assert not is_float(''.join(random.choice(string.ascii_letters) for _ in range(STRING_LEN)))

def test_calc_all_average(sums):
    all_sum = sum([x.get('sum') for x in sums.values()])
    counter = sum([x.get('count') for x in sums.values()])
    if counter == 0:
        assert 0 == calc_all_average(sums)
    assert (all_sum / counter) ==  calc_all_average(sums)

def test_calc_all_average_key_error(sums):
    with pytest.raises(TypeError):
        temp_sum = copy.deepcopy(sums)
        new_user = ''.join(random.choice(string.ascii_letters) for _ in range(STRING_LEN))
        while sums.has_key(new_user):
            new_user = ''.join(random.choice(string.ascii_letters) for _ in range(STRING_LEN))
        temp_sum[new_user] = {}
        calc_all_average(temp_sum)

def test_update_sums(sums):
    new_user = ''.join(random.choice(string.ascii_letters) for _ in range(STRING_LEN))
    rand_num = random.uniform(-1.0, 100.1)
    is_new = True
    if sums.has_key(new_user):
        is_new = False
    update_sums(sums, new_user, rand_num)
    if is_new:
        assert sums.get(new_user).get('sum') == rand_num
    update_sums(sums, new_user, random.uniform(-1.0, 100.1))
    assert True

def test_update_sums_new_user(sums):
    new_user = ''.join(random.choice(string.ascii_letters) for _ in range(STRING_LEN))
    rand_num = random.uniform(-1.0, 100.1)
    while sums.has_key(new_user):
        new_user = ''.join(random.choice(string.ascii_letters) for _ in range(STRING_LEN))
    update_sums(sums, new_user, rand_num)
    assert True


