#!/usr/bin/python

import argparse
import os
import pandas
import numpy

import gensim
from gensim import corpora
from gensim import similarities
from gensim.similarities import Similarity

import select_region
from select_region import select_region, sfname2index

import matplotlib.pyplot as plt
from pylab import *

from datetime import datetime

def average_weight4group(doc_ids,corpus):
	bow = []

	id2v = {}
	for di in doc_ids:
		for (i,v) in corpus[di]:
			if not i in id2v: id2v[i] = []
			id2v[i].append(v)

	for i in id2v:
		bow.append((i,numpy.mean(id2v[i])))

	return bow

def gen_sim_corpus(sim_file, query_bow):
	sim_index = Similarity.load(sim_file)
	sim_corpus = sim_index[query_bow]

	return sim_corpus

def viz_sim(sim_cor, dp_file, odir):
	smin = sim_cor.min(axis=0)
	smax = sim_cor.max(axis=0)

	print("Similarity min = %f, max = %f" % (smin, smax))

	dp_iterator = pandas.read_msgpack(dp_file, iterator = True)
	for ds_name, df in dp_iterator:
		max_x = df['x'].max()
		max_y = df['y'].max()
		arr = numpy.zeros([max_x+1, max_y+1])
			
		for row in df.itertuples():
			arr[row[1]][row[2]] = sim_cor[row[0]]

		plt.pcolormesh(arr, vmin=smin, vmax=smax, cmap='RdBu_r')
		plt.axes().set_aspect('equal', 'datalim')
		plt.axes().axis('off')
		plt.title(ds_name)
		plt.savefig(os.path.join(odir,ds_name.replace('/','!')), bbox_inches='tight')
		plt.clf()

def main():

	parser = argparse.ArgumentParser( description="Select pixels by ion intensity" )
	parser.add_argument( "--sf", help="The input subformula to id mapping.", required = True)
	parser.add_argument( "--dp", help="The input dataset to pixel cord mapping.", required = True)
	parser.add_argument( "--dsf", help="The input dataset to pixel sumformula mapping.", required = True)
	parser.add_argument( "-d", help="The input dataset name.", required = True)
	parser.add_argument( "-s", help="The input sumformula name.", required = True)
	parser.add_argument( "-a", help="The input adduct name.", required = True)
	parser.add_argument( "-i", help="The input threshold intensity.", type = int, default = -1)
	parser.add_argument( "-c", help="The input corpus file.", required = True)
	parser.add_argument( "--sim", help="The input similarity model file.", required = True)
	parser.add_argument( "-o", help="The output dir for images.", default = None)

	pa = parser.parse_args()

	ion_id = sfname2index(pa.sf, pa.s, pa.a.lstrip())

	pixel_ids = select_region(pa.dsf, pa.d, ion_id, pa.i)
	print(str(datetime.now()) + ': pixel_ids selected')
	corpus = gensim.corpora.MmCorpus(pa.c)
	query_bow = average_weight4group(pixel_ids,corpus)
	corpus = None
	pixel_ids = None
	print(str(datetime.now()) + ': query_bow generated')
	sim_corpus = gen_sim_corpus(pa.sim, query_bow)
	print(str(datetime.now()) + ': sim_corpus generated')
	viz_sim(sim_corpus,pa.dp, pa.o)

if __name__ == "__main__":
    main()