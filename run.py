#!/usr/bin/env python
import sys
import numpy as np
from sklearn.metrics import accuracy_score
from hmm import HMM
from read import read_annotations_from_file
from read import load_epochs_from_file
from feature_extraction import features_to_codebook
from feature_extraction import extract_features_from_epochs
import warnings

# Main
# run: python src/dhmm.py data/SC4001E0-PSG.edf data/annotations.txt
# ====
if __name__ == '__main__':
    
	warnings.filterwarnings("ignore")
	edf_file = 'SC4012E0-PSG.edf'
	annotations_file = '30secepoch1.csv'

	sleep_stages_dict = {'W':5, '1':3, '2':2, '3':1,
	'4':0, 'R':4, '?':6}
	sleep_stages = read_annotations_from_file(annotations_file, sleep_stages_dict)
	nr_states = len(np.unique(sleep_stages))
	# annotations contain long sequences of the awake state at the beginning and the end - those are removed
	actual_sleep_epochs_indices = np.where(sleep_stages != 5)
	sleep_start_index = actual_sleep_epochs_indices[0][0]
	sleep_end_index = actual_sleep_epochs_indices[0][-1]
	sleep_stages = sleep_stages[sleep_start_index:sleep_end_index]

	epochs = load_epochs_from_file(edf_file, epoch_length = 30, fs = 100)
	epochs = epochs[sleep_start_index:sleep_end_index,:]

	features = extract_features_from_epochs(epochs, epoch_length = 30, fs = 100)
	nr_groups = 20 # number of discrete features groups
	codebook, epoch_codes = features_to_codebook(features, nr_groups)

	training_percentage = 0.8 # % of data used for training the model
	sleep_stages_train, sleep_stages_test = np.split(sleep_stages, [int(training_percentage * sleep_stages.shape[0])])         
	epoch_codes_train, epoch_codes_test = np.split(epoch_codes, [int(training_percentage * epoch_codes.shape[0])]) 

	hmm = HMM(nr_states, nr_groups)
	hmm.train(sleep_stages_train, epoch_codes_train)
	x=hmm.get_state_sequence(epoch_codes_test)

	sleep_stages_reverse = {y:x for x,y in sleep_stages_dict.items()}
	actual_phases = list(map(lambda phase: sleep_stages_reverse[phase], sleep_stages_test))
	predicted_phases = list(map(lambda phase: sleep_stages_reverse[phase], x))
	print("Actual sleep phases paired with predicted sleep phases:")
	for actual, predicted in zip(actual_phases, predicted_phases):
		print(actual, predicted)
	print("Accuracy:", accuracy_score(sleep_stages_test, x))