import sys
import time, random
sys.path.append("..")
from abtest import ABTest

if __name__ == "__main__":
    ab = ABTest()
    ab.parse_from_xml("abtest.xml")
    exp_data = {}
    layer_data = {}
    S = list("abcdefghijklmnopqrstuvwxyz!@#$%^&*()")
    Num = 1000000
    ids = [''.join(random.sample(S, 5)) for i in range(Num)]
    t0 = time.time()
    print("Start To Cal")
    for i in range(Num):
        exp_id, _, layered, layers = ab.get_exp(ids[i])
        if exp_id in exp_data:
            exp_data[exp_id] += 1
        else:
            exp_data[exp_id] = 1
            layer_data[exp_id] = {}
        if layered:
            for layer_id, layer_name, sub_layer_id, sub_layer_name in layers:
                if "%d:%d"%(layer_id, sub_layer_id) in layer_data[exp_id]:
                    layer_data[exp_id]["%d:%d"%(layer_id, sub_layer_id)] += 1
                else:
                    layer_data[exp_id]["%d:%d"%(layer_id, sub_layer_id)] = 1
    t1 = time.time()
    print("Cost %3.4f, Avg %d/S"%(t1 - t0, Num / (t1 - t0)))
    for exp_id in exp_data:
        print("ExpId(%-2d) Num(%-7d) Rate(%-2.3f) "%(exp_id, exp_data[exp_id], float(exp_data[exp_id])/Num))
        if exp_id in layer_data:
            for layer_id in layer_data[exp_id]:
                print("         ExpId(%-2d) LayerId(%3s) Num(%-7d) Rate(%-2.3f)"%(
                    exp_id,
                    layer_id,
                    layer_data[exp_id][layer_id],
                    float(layer_data[exp_id][layer_id])/Num))
    print("End To Cal")


