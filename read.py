import numpy as np
import pyedflib

def read_annotations_from_file(filename, sleep_stages_dict):
    print("Reading annotations...")
    with open(filename) as f:
        content = f.readlines()    
    sleep_stages = []
    for index in range(0, len(content)):
        tokens = content[index].split()
    #    print(tokens)
        if(len(tokens)==3 and tokens[2]!='?'):
#            print(sleep_stages_dict.get(tokens[2]))
            sleep_stages =  sleep_stages + [(sleep_stages_dict.get(tokens[2]))]
    sleep_stages  =  sleep_stages + [6]
    sleep_stages = sleep_stages + [6]
#    print(sleep_stages)
    sleep_stages = np.array(sleep_stages)
#    print(sleep_stages)
    return sleep_stages

def load_epochs_from_file(filename, epoch_length, fs):
    print("Loading epochs...")
    # fs: sampling frequency
    f = pyedflib.EdfReader(filename)
    n = f.signals_in_file
    signal_labels = f.getSignalLabels()
    sigbuf = f.readSignal(0)
    print(sigbuf)
    L = epoch_length * fs # signal length
    epochs = np.reshape(sigbuf, (-1, L))
    return epochs



