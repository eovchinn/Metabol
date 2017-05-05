#!/usr/bin/python

import argparse
import pandas as pd
import matplotlib.pyplot as plt
from pylab import *
import numpy
import os

def sfname2index(sf_file, sf_name, add_name):
	sumformulas = pd.read_msgpack(sf_file)
	if (len(add_name)>0):
		sf_index = sumformulas[(sumformulas.sf == sf_name) & (sumformulas.adduct == add_name)].index.tolist()
	else: sf_index = sumformulas[sumformulas.sf == sf_name].index.tolist()
	sumformulas = None

	return sf_index

def select_region(dsf_file, ds_name, ion_id, quan, i):
	ds_iterator = pd.read_msgpack(dsf_file, iterator = True)
	for name, df in ds_iterator:
		if name == ds_name:
			ion_rows = df.loc[df['ion_id'] == ion_id]
			if i<0: 
				ints = ion_rows['int'].tolist()
				q = numpy.percentile(ints,quan)
				i = q#/2
			rel_rows = ion_rows.loc[ion_rows['int'] > i]
			pixel_ids = rel_rows['p_id'].tolist()
			return pixel_ids

	return []

def viz_region(dp_file, pixel_ids, ds_name, ion_name, odir):
	dp_iterator = pd.read_msgpack(dp_file, iterator = True)
	for name, df in dp_iterator:
		if name == ds_name:
			max_x = df['x'].max()
			max_y = df['y'].max()
			arr = numpy.zeros([max_x+1, max_y+1])

			for pid in pixel_ids:
				rel_row = df.loc[pid]
				arr[rel_row['x']][rel_row['y']] = 1

			arr = np.rot90(arr, 1)
			plt.pcolormesh(arr,cmap='viridis')
			plt.axes().set_aspect('equal', 'datalim')
			plt.axes().axis('off')
			fname =  ds_name + '_' + ion_name
			plt.title(fname)

			if odir:
				plt.savefig(os.path.join(odir,fname.replace('/','!')), bbox_inches='tight')
			else: plt.show()

			break

def draw_dataset_ion(dsf_file, dp_file, ds_name, ion_id, odir):
	# find quantile intensity
	ds_iterator = pd.read_msgpack(dsf_file, iterator = True)
	for name, df in ds_iterator:
		if name == ds_name:
			ion_rows = df.loc[df['ion_id'] == ion_id]
			q = np.percentile(ion_rows.int,95)
			#print(q)
			break

	dp_iterator = pd.read_msgpack(dp_file, iterator = True)
	for name, df in dp_iterator:
		if name == ds_name:
			max_x = df['x'].max()
			max_y = df['y'].max()

			arr = numpy.zeros([max_x+1, max_y+1])

			#print(numpy.min(df.index.values),numpy.max(df.index.values),len(df.index.values))

			for ir in ion_rows.itertuples():
				pid = ir[1]
				i = ir[3]

				rel_row = df.loc[pid]
				arr[rel_row['x']][rel_row['y']] = i

			arr[arr > q] = q
			arr = np.rot90(arr, 1)

			plt.pcolormesh(arr,cmap='viridis')
			plt.axes().set_aspect('equal', 'datalim')
			plt.axes().axis('off')
			fname =  ds_name + '_' + str(ion_id)
			plt.title(fname)

			if odir: 
				plt.savefig(os.path.join(odir,fname.replace('/','!')), bbox_inches='tight')
				plt.clf()
			else: plt.show()

			break
def main():

	parser = argparse.ArgumentParser( description="Select pixels by ion intensity" )
	parser.add_argument( "--pa", help="The input pixel annotation file.")
	parser.add_argument( "--sf", help="The input subformula to id mapping.", required = True)
	parser.add_argument( "--dp", help="The input dataset to pixel cord mapping.", required = True)
	parser.add_argument( "--dsf", help="The input dataset to pixel sumformula mapping.", required = True)
	parser.add_argument( "-d", help="The input dataset name.", required = True)
	parser.add_argument( "-s", help="The input sumformula name.", required = True)
	parser.add_argument( "-a", help="The input adduct name.", required = True)
	parser.add_argument( "-i", help="The input threshold intensity.", type = int, default = -1)
	parser.add_argument( "-o", help="The output dir for images.", default = None)

	pa = parser.parse_args()

	ion_id = sfname2index(pa.sf, pa.s, pa.a.lstrip())

	#print(ion_id)

	draw_dataset_ion(pa.dsf, pa.dp, pa.d, ion_id, pa.o)

	#pixel_ids = select_region(pa.dsf, pa.d, ion_id, pa.i)
	#viz_region(pa.dp, pixel_ids, pa.d, pa.s+pa.a, pa.o)

if __name__ == "__main__":
    main()