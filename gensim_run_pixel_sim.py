#!/usr/bin/python

import argparse
import os
import pandas

import gensim
from gensim import similarities
from gensim.similarities import Similarity
from gensim import corpora

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def main():

	parser = argparse.ArgumentParser( description="generate pixel similarity indexes" )
	parser.add_argument( "-c", help="The input corpus (.mm).", required = True)	
	parser.add_argument( "--sim", help="The output file with sim model (.index).", required = True)
	parser.add_argument( "--opref", help="Output prefix.", required = True)	
	parser.add_argument( "--simmat", help="The output file with sim matrix (.mm).")

	pa = parser.parse_args()

	corpus = gensim.corpora.MmCorpus(pa.c)

	sim_index = gensim.similarities.docsim.Similarity(pa.opref, corpus, num_features = corpus.num_terms)
	sim_index.save(pa.sim)

	if pa.simmat:
		sim_matrix = sim_index[corpus]
		with open(pa.simmat, 'wb') as f: pickle.dump(sim_matrix, f)
		

if __name__ == "__main__":
    main()