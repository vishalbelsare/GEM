import numpy as np
from subprocess import call
from gem.embedding.static_graph_embedding import StaticGraphEmbedding
from gem.utils import graph_util


class node2vec(StaticGraphEmbedding):

    def __init__(self, *hyper_dict, **kwargs):
        """ Initialize the node2vec class

        Args:
            d: dimension of the embedding
            max_iter: max iterations
            walk_len: length of random walk
            num_walks: number of random walks
            con_size: context size
            ret_p: return weight
            inout_p: inout weight
        """
        hyper_params = {
            'method_name': 'node2vec_rw'
        }
        hyper_params.update(kwargs)
        for key in hyper_params.keys():
            self.__setattr__('_%s' % key, hyper_params[key])
        for dictionary in hyper_dict:
            for key in dictionary:
                self.__setattr__('_%s' % key, dictionary[key])

    def get_method_name(self):
        return self._method_name

    def get_method_summary(self):
        return '%s_%d' % (self._method_name, self._d)

    def learn_embedding(self, graph=None, edge_f=None,
                        is_weighted=False, no_python=False):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        executable = os.path.abspath(os.path.join(current_dir, '../c_exe/node2vec'))
        args = [executable]
        if not graph and not edge_f:
            raise Exception('graph/edge_f needed')
        if edge_f:
            graph = graph_util.loadGraphFromEdgeListTxt(edge_f)
        graph_util.saveGraphToEdgeListTxtn2v(graph, 'tempGraph.graph')
        args.append("-i:tempGraph.graph")
        args.append("-o:tempGraph.emb")
        args.append("-d:%d" % self._d)
        args.append("-l:%d" % self._walk_len)
        args.append("-r:%d" % self._num_walks)
        args.append("-k:%d" % self._con_size)
        args.append("-e:%d" % self._max_iter)
        args.append("-p:%f" % self._ret_p)
        args.append("-q:%f" % self._inout_p)
        args.append("-v")
        args.append("-dr")
        args.append("-w")
        try:
            call(args)
        except Exception as e:
            print(str(e))
            raise Exception('./node2vec not found. Please compile snap, place node2vec in the system path '
                            'and grant executable permission')
        self._X = graph_util.loadEmbedding('tempGraph.emb')
        return self._X

    def get_embedding(self):
        return self._X

    def get_edge_weight(self, i, j):
        return np.dot(self._X[i, :], self._X[j, :])
