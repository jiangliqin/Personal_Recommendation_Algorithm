# -*- coding:utf-8 -*-
"""
@Author：Charles Van
@E-mail:  williananjhon@hotmail.com
@Time：2019-06-16 20:05
@Project:Personal_Recommendation_Algorithm
@Filename:content_based.py
"""


from __future__ import division
import os
import operator
import sys
sys.path.append("../util")
import util.CB_read as read

def get_up(item_cate,input_file):
	"""
	:param item_cate: key itemid, value: dict, key category value ratio
	:param input_file: user rating file
	:return:
		a dict: key userid, value:[(category,ratio),(category1,ratio1)]
	"""
	if not os.path.exists(input_file):
		return {}
	record = {}
	up = {}
	score_thr = 4.0
	topK = 2
	fp = open(input_file,encoding="utf-8")
	for line in fp:
		item = line.strip().split("::")
		if len(item) < 4:
			continue
		userid,itemid,rating,timestamp = item[0],item[1],float(item[2]),int(item[3])
		if rating < score_thr:
			continue
		if itemid not in item_cate:
			continue
		time_score = get_time_score(timestamp)
		if userid not in record:
			record[userid] = {}
		for fix_cate in item_cate[itemid]:
			if fix_cate not in record[userid]:
				record[userid][fix_cate] = 0
			record[userid][fix_cate] += rating * time_score * item_cate[itemid][fix_cate]
	fp.close()
	for userid in record:
		if userid not in up:
			up[userid] = []
		total_score = 0
		for zuhe in sorted(record[userid].items(),key=operator.itemgetter(1),reverse=True)[:topK]:
			up[userid].append((zuhe[0],zuhe[1]))
			total_score += zuhe[1]
		for index in range(len(up[userid])):
			up[userid][index] = (up[userid][index][0],round(up[userid][index][1] / total_score,3))
	return up


def get_time_score(timestamp):
	"""
	:param timestamp: input timestamp
	:return:
		time score
	"""
	fix_time_stamp = 1046454590
	total_sec = 24 * 60 * 60
	delta = (fix_time_stamp - timestamp) / total_sec / 100
	return round(1 / (1 + delta),3)


def recom(cate_item_sort,up,userid,topK=10):
	"""
	:param cate_item_sort: reverse sort
	:param up: user profile
	:param userid: userid to recom
	:param topK: recom num
	:return:
		a dict, key userid, value[itemid1,itemid2]
	"""
	if userid not in up:
		return {}
	recom_result = {}
	if userid not in recom_result:
		recom_result[userid] = []
	for zuhe in up[userid]:
		cate = zuhe[0]
		ratio = zuhe[1]
		num = int(topK * ratio) + 1
		if cate not in cate_item_sort:
			continue
		recom_list = cate_item_sort[cate][:num]
		recom_result[userid] += recom_list
	return recom_result


def run_main():
	ave_score = read.get_ave_score("../data/ratings.dat")
	item_score,cate_item_sort = read.get_item_cate(ave_score,"../data/movies.dat")
	up = get_up(item_score,"../data/ratings.dat")
	print(len(up))


if __name__ == "__main__":
	run_main()