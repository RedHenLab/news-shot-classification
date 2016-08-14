import os, sys
import fnmatch
import googlenet
import fileops
import cropframes
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

def testset(clip_dir, fc7_file):

	test_features = []

	with open(clip_dir + fc7_file) as features_file:
		features = features_file.readlines()
	features = [feature.split('\n')[0] for feature in features]
	test_features += features

	return test_features

def ovo_trainset(train_labels, class_type):
	
	new_train_labels = []
	if class_type == 'newsperson':
		for label in train_labels:
			if label != 'Newsperson(s)':
				label = 'Not'
			new_train_labels.append(label)
	elif class_type == 'broll':
		for label in train_labels:
			if label != 'Background_roll':
				label = 'Not'
			new_train_labels.append(label)		

	return new_train_labels


def trainset(main_dir, annotations_file, fc7_file):

	dir_list = sorted(os.listdir(main_dir))

	features_data = []
	label_data = []

	for dir_name in dir_list:
		if os.path.isdir(main_dir + dir_name):
			if os.path.exists(main_dir + dir_name + '/' + dir_name + annotations_file):

				with open(main_dir + dir_name + '/' + dir_name + annotations_file) as labels_file:
					labels = labels_file.readlines()
				labels = [label.split('\t')[0] for label in labels]
				label_data += labels

				with open(main_dir + dir_name + '/' + fc7_file) as features_file:
					features = features_file.readlines()
				features = [feature.split('\n')[0] for feature in features]
				features_data += features

	## To exclude Commercial class etc.
	labels = []
	features = []
	news = 0
	bg = 0
	g = 0
	w = 0
	sp = 0
	c = 0
	p = 0
	r = 0
	h = 0
	s = 0
	for idx, label in enumerate(label_data):
		if label not in ['Commercial','Problem/Unclassified']:
			if label == 'Reporter':
				label = 'Newsperson(s)'
				r += 1
			if label == 'Hybrid':
				label = 'Newsperson(s)'
				h += 1
			if label == 'Studio':
				label = 'Newsperson(s)'
				s += 1
			elif label == 'Background_roll' or label == 'Talking_head' or label == 'Talking_head/Hybrid':	
				label = 'Background_roll'
				bg += 1
			elif label == 'Graphic':
				g += 1
			elif label == 'Weather':
				w += 1
			elif label == 'Sports':
				sp += 1
			labels.append(label)
			features.append(features_data[idx])
			
		else:
			if label == 'Commercial':
				c += 1
			elif label == 'Problem/Unclassified':
				p += 1

	print len(labels)
	print news, s, r, h, bg, g, w, sp, c, p

	return features, labels