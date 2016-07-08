import os, sys, time
os.environ["GLOG_minloglevel"] = "2"
import fileops
import keyframes
import shotdetect
import facedetect
import placesCNN
import googlenet
import age_genderCNN
import graphcluster, accuracy
import dataset, classifier
import pipeline
# import cropframes

def main():
	root = '/home/shruti/gsoc/news-shot-classification/'

	# clip_dir = '/home/shruti/gsoc/news-shot-classification/full-clips/2016-06-07_0000_US_CNN_Anderson_Cooper_360_0-3595/'
	clip_dir = '/home/shruti/gsoc/news-shot-classification/full-clips/2016-06-07_0100_US_KABC_Eyewitness_News_6PM_0-1793/'
	# clip_dir = '/home/shruti/gsoc/news-shot-classification/full-clips/2016-06-07_0000_US_FOX-News_The_OReilly_Factor_0-3595/'
	# clip_dir = '/home/shruti/gsoc/news-shot-classification/full-clips/2016-06-07_0100_US_KCBS_CBS_2_News_at_6_0-1735/'
	
	# clip_dir = '/home/shruti/gsoc/news-shot-classification/full-clips/2016-06-21_0000_UK_KCET_BBC_World_News_America/'
	# clip_dir = '/home/shruti/gsoc/news-shot-classification/full-clips/2016-06-21_0000_US_CNN_Anderson_Cooper_360/'
	# clip_dir = '/home/shruti/gsoc/news-shot-classification/full-clips/2016-06-21_0600_US_KABC_KABC_7_News_at_11PM'
	# clip_dir = '/home/shruti/gsoc/news-shot-classification/full-clips/2016-06-21_0600_US_KCBS_CBS_2_News_at_11PM'
	# clip_dir = '/home/shruti/gsoc/news-shot-classification/full-clips/2016-06-21_0000_US_FOX-News_The_OReilly_Factor'
	# clip_dir = '/home/shruti/gsoc/news-shot-classification/full-clips/2016-06-21_1100_US_KNBC_Early_Today'

	# clip_dir = '/home/shruti/gsoc/news-shot-classification/full-clips/2014-01-31_0230_US_KNBC_NBC_Nightly_News'
	# clip_dir = '/home/shruti/gsoc/news-shot-classification/full-clips/2014-05-10_2200_US_CNN_Situation_Room'
	# clip_dir = '/home/shruti/gsoc/news-shot-classification/full-clips/2014-05-10_0000_US_CNN_Anderson_Cooper_360'
	# clip_dir = '/home/shruti/gsoc/news-shot-classification/full-clips/2014-05-10_2300_US_KABC_Eyewitness_News_4PM'
	# clip_dir = '/home/shruti/gsoc/news-shot-classification/full-clips/2016-06-21_1000_US_MSNBC_Morning_Joe'
	
	# clip_dir = '/home/shruti/gsoc/news-shot-classification/full-clips/2016-06-21_0635_US_KABC_Jimmy_Kimmel_Live'
	# clip_dir = '/home/shruti/gsoc/news-shot-classification/full-clips/2016-07-01_0000_US_HLN_Nancy_Grace'
	
	if clip_dir[-1] is not '/':
		clip_dir = clip_dir + '/'
		print clip_dir
	
	overall_start = time.time()

	output_filename = clip_dir.split('/')[-2]	
	# clip_name = fileops.get_video_filename(clip_dir)
	# shotdetect.shotdetect(clip_dir, clip_name)
	# keyframes.get_keyframes(clip_dir, clip_name, output_filename)

	image_files = fileops.get_keyframeslist(clip_dir)
	# image_files = cropframes.cropframes(clip_dir, image_files)
	#image_files = ['/home/shruti/gsoc/news-shot-classification/clips/2016-05-22_2300_US_KABC_Eyewitness_News_4PM_0-465/keyframe039.jpg']

	# studio_shots = graphcluster.get_graph_clusters(clip_dir, image_files)
	# print studio_shots
	# print len(studio_shots)
	# fileops.save_studio(clip_dir + output_filename, studio_shots)
	## Run a model and get labels for keyframe
 	
	caffe_path = '/home/shruti/gsoc/caffehome/caffe/' 
		
	# [pool5, conv5, conv4, conv3,fc8, fc7, fc6, output_label_list, scene_type_list, label_list, scene_attributes_list] = placesCNN.placesCNN(caffe_path, caffe_path + 'models/placesCNN/', image_files)
	[pool5, conv5, conv4, conv3] = placesCNN.placesCNN(caffe_path, caffe_path + 'models/placesCNN/', image_files)

	# accuracy.get_accuracy(clip_dir + output_filename, '_scene', scene_type_list)
	# fileops.save_placesCNN_labels(clip_dir + output_filename, clip_dir + 'placesCNN_labels', output_label_list, scene_type_list, label_list, scene_attributes_list)
	
	# fileops.save_features(clip_dir + 'new_places_pool5', pool5)
	# print "Done pool5"
	# fileops.save_features(clip_dir + 'new_places_conv5', conv5)
	# print "done conv5"
	# fileops.save_features(clip_dir + 'new_places_conv4', conv4)
	# print "done conv4"
	# fileops.save_features(clip_dir + 'new_places_conv3', conv3)
	# print "done conv3"
	# fileops.save_features(clip_dir + 'new_places_fc8', fc8)
	# print "Done fc8"
	# fileops.save_features(clip_dir + 'new_places_fc7 ', fc7)
	# print "done fc7"
	# fileops.save_features(clip_dir + 'new_places_fc6', fc6)
	# print "done fc6"

	# label_list = googlenet.googlenet(caffe_path, caffe_path + 'models/bvlc_googlenet/', image_files)
	# fileops.save_googlenet_labels(clip_dir + output_filename, clip_dir + 'googlenet_labels', label_list)

	# fileops.write_separate_labels(clip_dir + output_filename)

	train_dir = '/home/shruti/gsoc/news-shot-classification/full-clips/train/'
	test_dir = '/home/shruti/gsoc/news-shot-classification/full-clips/test/'
	
	# pipeline.pipeline(train_dir, test_dir)
	
	overall_end = time.time()	
	print "Total time taken: %.2f" %(overall_end-overall_start)

if __name__ == '__main__':
	main()