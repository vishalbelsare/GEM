from abc import ABCMeta
import numpy as np


class StaticGraphEmbedding:
	__metaclass__ = ABCMeta

	def __init__(self, d):
		"""Initialize the Embedding class

		Args:
			d: dimension of embedding
		"""
		pass

	def get_method_name(self):
		""" Returns the name for the embedding method

		Return:
			The name of embedding
		"""
		return ''

	def get_method_summary(self):
		""" Returns the summary for the embedding include method name and paramater setting

		Return:
			A summary string of the method
		"""
		return ''

	def learn_embedding(self, graph):
		"""Learning the graph embedding from the adjcency matrix.

		Args:
			graph: the graph to embed in networkx DiGraph format
		"""
		pass

	def get_embedding(self):
		""" Returns the learnt embedding

		Return:
			A numpy array of size #nodes * d
		"""
		pass

	def get_edge_weight(self, i, j):
		"""Compute the weight for edge between node i and node j

		Args:
			i, j: two node id in the graph for embedding
		Returns:
			A single number represent the weight of edge between node i and node j

		"""
		pass

	def get_reconstructed_adj(self, X=None, node_l=None):
		"""Compute the adjacency matrix from the learned embedding

		Returns:
		    A numpy array of size #nodes * #nodes containing the reconstructed adjacency matrix.
		"""
		if X is not None:
			node_num = X.shape[0]
			self._X = X
		else:
			node_num = self._node_num
		adj_mtx_r = np.zeros((node_num, node_num))
		for v_i in range(node_num):
			for v_j in range(node_num):
				if v_i == v_j:
					continue
				adj_mtx_r[v_i, v_j] = self.get_edge_weight(v_i, v_j)
		return adj_mtx_r
