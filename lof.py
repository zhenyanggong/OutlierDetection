import string
import sys
import os
import random
import collections
import csv

def cal_distance(str1, str2):
	# calculate distance between two point
	if (len(str1) != len(str2)):
		print("cal distance error!!!")
	distance = 0.0
	for i in range(len(str1)):
		a = float(str1[i])
		b = float(str2[i])
		distance += (a - b)**(2)
	distance = distance**(1/2)
	return distance


def get_command():
# get command line argument
	input_path = ""
	output_path = ""
	k = 0
	cutoff = 0.0
	for i in range(len(sys.argv)):
		if sys.argv[i] == "--input_path":
			j = i + 1
			input_path = sys.argv[j]
		elif sys.argv[i] == "--output_path":
			j = i + 1
			output_path = sys.argv[j]
		elif sys.argv[i] == "-k":
			j = i + 1
			k = int(sys.argv[j])
		elif sys.argv[i] == "-cutoff":
			j = i + 1
			cutoff = float(sys.argv[j])
	return input_path, output_path, k, cutoff

def get_document(input_path):
	content = []
	document_map = {}
	with open(input_path) as f:
		content = f.read().splitlines()
	for row in content:
		index = row.split(',', 1)[0]
		features = (row.split(',', 1)[1]).split(",")
		document_map[index] = features
	return document_map

def get_neighbor(document_map, k):
	# double for loop to calculate distance between each pair of points
	# distance map is a dict of dict store all distance among points
	distance_map = {}
	# neighbor map is a dict of list store all k-neighbors of that point
	neighbors_map = {}
	# it stores kth neighbor distance
	k_distance_map = {}
	for key1, value1 in document_map.items():
		temp = {}
		for key2, value2 in document_map.items():
			if key1 != key2:
				# for two different points, cal distance
				temp[key2] = cal_distance(document_map[key1], document_map[key2])
				if temp[key2] == 0.0:
					print(key1)
					print(key2)
		distance_map[key1] = temp
	#print(distance_map)
	for key1, value1 in distance_map.items():
		# sort the key
		# sort_values = sorted(distance_map[key1].values())
		#print(distance_map[key1])
		sort_values = sorted(distance_map[key1], key=distance_map[key1].get)
		#print(sort_values)
		k_value = sort_values[k-1]
		#print(k_value)
		k_distance = distance_map[key1][k_value]
		k_distance_map[key1] = k_distance
		for key2, value2 in value1.items():
			if value2 <= k_distance:
				if key1 not in neighbors_map:
					neighbors_map[key1] = [key2]
				else:
					neighbors_map[key1].append(key2)
	return distance_map, neighbors_map, k_distance_map

def get_lof(distance_map, neighbors_map, k_distance_map):
	ar_map = {}
	lof_map = {}
	for key1, value1 in neighbors_map.items():
		sumOfAr = 0.0
		for key2 in value1:
			ar = max(distance_map[key1][key2], k_distance_map[key2])
			if ar == 0.0:
				print(key1)
				print(key2)
			sumOfAr += ar
		avg_ar = sumOfAr / (len(value1))
		ar_map[key1] = avg_ar
	#print(ar_map)
	for key1, value1 in neighbors_map.items():
		sumOfLof = 0.0
		for key2 in value1:
			if ar_map[key2] == 0.0:
				sumOfLof += 0.0
			else :
				sumOfLof += (ar_map[key1] / ar_map[key2])
		avg_lof = sumOfLof / len(value1)
		lof_map[key1] = avg_lof
	return lof_map



def main():
	input_path, output_path, k, cutoff = get_command()
	document_map = get_document(input_path)
	distance_map, neighbors_map, k_distance_map = get_neighbor(document_map, k)
	lof_map = get_lof(distance_map, neighbors_map, k_distance_map)
	with open(output_path,'w') as file:
		writer = csv.writer(file)
		for key, value in document_map.items():
			if lof_map[key] > cutoff:
				writer.writerow([key, 1])
			else:
				writer.writerow([key, 0])
	file.close()
	



if __name__ == '__main__':
	main()