import os, sys, time, shutil
os.environ["GLOG_minloglevel"] = "2"
import fileops, cropframes
import keyframes, shotdetect
import placesCNN, googlenet
import dataset, classifier, cPickle
import format_output
# import graphcluster, accuracy


def main():
	overall_start = time.time()

	caffe_path = './mycaffe/'
	fpickle = './ovr_classifier.pkl'
	features_file = 'cropped_places_fc7 .csv'		

	## Test classifier accuracy
	if sys.argv[1] == 'testmode':

		fpickle = './test_newg_ovr_classifier.pkl'
		test_dir = './full-clips/test/'	
		train_dir = './full-clips/train/'
		annotation_file = '_new_shot_type_testuser.txt'
		class_type = 'newsperson'
		classifier.classifier_dump(fpickle, train_dir, annotation_file, features_file)

		with open(fpickle, 'r') as pickle_file:
			myclassifier = cPickle.load(pickle_file)
		[test_data, test_labels] = dataset.trainset(test_dir, annotation_file, features_file)
		# new_test_labels = dataset.ovo_trainset(test_labels, class_type)
		new_test_labels = test_labels
		output = classifier.predict_testmode(myclassifier, test_data, new_test_labels, test_labels)

		print "Classified frames...\n"

		# clip_dir = sys.argv[2]
		# broll_dir = './broll/'
		# new_dir = broll_dir + clip_dir + '/'
		# old_dir = train_dir + clip_dir + '/'

		# with open(old_dir + clip_dir + annotation_file, 'r') as forig:
		# 	labels = forig.readlines()
		# keyframes = [label.split('\t')[1] for label in labels]
		# labels = [label.split('\t')[0] for label in labels]

		# with open(new_dir + clip_dir + '_broll_testuser.txt', 'r') as fnew:
		# 	newlabels = fnew.readlines()
		# newkeyframes = [newlabel.split('\t')[1] for newlabel in newlabels]
		# newlabels = [newlabel.split('\t')[0] for newlabel in newlabels]

		# for newlabel, newkeyframe in zip(newlabels, newkeyframes):
		# 	if newkeyframe in keyframes:
		# 		idx = keyframes.index(newkeyframe)
		# 		labels[idx] = newlabel

		# lines = [label + '\t' + keyframe for label, keyframe in zip(labels, keyframes)]
		
		# with open(old_dir + clip_dir + '_new_shot_type_testuser.txt', 'w') as final:
		# 	final.writelines(lines)

	else:

		clip_path = sys.argv[1] 								## ../../dir/video.mp4
		rel_clip_path = clip_path.rsplit('/',1)[0] + '/'		## ../../dir/
		clip_name = clip_path.rsplit('/',1)[1]					## video.mp4
		clip = clip_name.rsplit('.',1)[0]						## video
		output_filename = clip 									## video
		clip_dir = rel_clip_path + clip + '/'					## ../../dir/video/

		if not os.path.exists(clip_dir):
			os.makedirs(clip_dir)
		else:
			shutil.rmtree(clip_dir)
			os.makedirs(clip_dir)
		shutil.copy(clip_path, clip_dir)
		new_clip_path = clip_dir + clip_name					## ../../dir/video/video.mp4

		keyframe_times = keyframes.keyframes(clip_dir, new_clip_path)
		keyframes_list = fileops.get_keyframeslist(clip_dir)
		shot_boundaries, py_times = shotdetect.shotdetect(clip_dir, new_clip_path)
		py_images = fileops.get_pyframeslist(clip_dir, clip_name)
		
		orig_images, all_timestamps = fileops.rename_frames(clip_dir, keyframe_times, keyframes_list, py_times, py_images)
		if features_file == 'cropped_places_fc7 .csv':
			image_files = cropframes.cropframes(clip_dir, orig_images)
			for image in orig_images:
				os.remove(image)
		else:
			image_files = orig_images

		os.remove(clip_dir + clip_name)
		print "Video preprocessing done...\n"
		
		## Run a model and get labels for keyframe
		[fc7, scene_type_list, places_labels, scene_attributes_list] = placesCNN.placesCNN(caffe_path, caffe_path + 'models/placesCNN/', image_files)
		fileops.save_features(clip_dir + features_file, fc7)
		print "Extracted fc7 features...\n"

		with open(fpickle, 'r') as pickle_file:
			myclassifier = cPickle.load(pickle_file)
		test_data = dataset.testset(clip_dir, features_file)
		classifier_label_list = classifier.classifier_predict(myclassifier, test_data)
		print "Classified frames...\n"

		os.remove(clip_dir + features_file)

		[googlenet_cat, googlenet_labels] = googlenet.googlenet(caffe_path, caffe_path + 'models/bvlc_googlenet/', image_files)
		print "Retrieved imagenet labels...\n"

		format_output.output_labels(rel_clip_path + output_filename, all_timestamps, image_files, shot_boundaries, classifier_label_list, googlenet_cat, googlenet_labels, scene_type_list, places_labels, scene_attributes_list)
		
		shutil.rmtree(clip_dir)

	overall_end = time.time()	
	print "Total time taken: %.2f" %(overall_end-overall_start)

if __name__ == '__main__':
	main()