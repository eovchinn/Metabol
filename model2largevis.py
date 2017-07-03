#!/usr/bin/python

import argparse

def largevisformat(c_file, s_file, o_file):
	import gensim

	ofile = open(o_file, 'w')

	from gensim import corpora	
	corpus = gensim.corpora.MmCorpus(c_file)

	if s_file:
		from gensim import similarities
		from gensim.similarities import Similarity
		sim_index = Similarity.load(s_file)

		i = 0
		for doc1 in corpus:
			sims = sim_index[doc1]
			j = 0
			for s in sims:
					dist = s
					ofile.write("%d %d %f\n" % (i,j,dist))
					j+=1
			i+=1
	else:
		ofile.write("%d %d\n" %  (corpus.num_docs, corpus.num_terms))
		#ofile.write("%d %d\n" %  (10000, corpus.num_terms))

		counter = 0
		for doc in corpus:
			doc.sort(key=lambda x: x[0],reverse=False)
			ps = 0
			for (s, w) in doc:
				for i in range(0,(s-ps)):
					ofile.write('0.0 ')
				ofile.write('%f ' % (w))
				ps = s
			counter+=1
			#if (counter == 10000): break	
			#ofile.write('\n')



def largevisproc(i_file, o_file, sim):
	import LargeVis

	outdim = 2
	threads = 24
	samples = -1
	prop = -1
	alpha = -1
	trees = -1
	neg = -1
	neigh = -1
	gamma = -1
	perp = -1

	if sim: LargeVis.loadgraph(i_file)
	else: LargeVis.loadfile(i_file)

	Y = LargeVis.run(outdim, threads, samples, prop, alpha, trees, neg, neigh, gamma, perp)

	LargeVis.save(o_file)

def largevislabel(o_file, pa_file):
	import pandas as pd

	ofile = open(o_file, 'w')
	pixel_iterator = pd.read_msgpack(pa_file, iterator = True)

	counter = 0
	for d, df in pixel_iterator:
		ofile.write('%d' % (d['ds_id']))
		counter+=1
		if (counter == 10000): break
		ofile.write('\n')

def main():

	parser = argparse.ArgumentParser( description="Select pixels by ion intensity" )
	parser.add_argument( "-c", help="The input corpus file.", default = None)
	parser.add_argument( "-s", help="The input similarity file.", default = None)
	parser.add_argument( "--lv", help="The output LargeVis file.", required = True)
	parser.add_argument( "--lv2d", help="The output LargeVis 2D file.", required = True)
	parser.add_argument( "--pa", help="The input pixel annotation file.")
	parser.add_argument( "--lvl", help="Label file for LarveVis.")


	pa = parser.parse_args()


	#largevisformat(pa.c, pa.s, pa.lv)
	largevisproc(pa.lv, pa.lv2d, pa.s)
	#largevislabel(pa.lvl,pa.pa)

if __name__ == "__main__":
    main()