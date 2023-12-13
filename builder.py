
"""Graph builder from pandas dataframes"""
from collections import namedtuple
from pandas.api.types import is_numeric_dtype, is_categorical_dtype, is_categorical
import dgl
import torch

__all__ = ['PandasGraphBuilder']

def _series_to_tensor(series):
    if is_categorical(series):
        return torch.LongTensor(series.cat.codes.values.astype('int64'))
    else:       # numeric
        return torch.FloatTensor(series.values)

class PandasGraphBuilder(object):
    """Creates a heterogeneous graph from multiple pandas dataframes.
    """
    def __init__(self):
        self.entity_tables = {}
        self.relation_tables = {}
        self.entity_pk_to_name = {}     
        self.entity_pk = {}           
        self.entity_key_map = {}        
        self.num_nodes_per_type = {}
        self.edges_per_relation = {}
        self.relation_name_to_etype = {}
        self.relation_src_key = {}     
        self.relation_dst_key = {}   

    def add_entities(self, entity_table, primary_key, name):
        entities = entity_table[primary_key].astype('category')
        if not (entities.value_counts() == 1).all():
            raise ValueError('Different entity with the same primary key detected.')
        # preserve the category order in the original entity table
        entities = entities.cat.reorder_categories(entity_table[primary_key].values)

        self.entity_pk_to_name[primary_key] = name
        self.entity_pk[name] = primary_key
        self.num_nodes_per_type[name] = entity_table.shape[0]
        self.entity_key_map[name] = entities
        self.entity_tables[name] = entity_table

    def add_binary_relations(self, relation_table, source_key, destination_key, name):
        src = relation_table[source_key].astype('category')
        src = src.cat.set_categories(
            self.entity_key_map[self.entity_pk_to_name[source_key]].cat.categories)
        dst = relation_table[destination_key].astype('category')
        dst = dst.cat.set_categories(
            self.entity_key_map[self.entity_pk_to_name[destination_key]].cat.categories)
        if src.isnull().any():
            raise ValueError(
                'Some source entities in relation %s do not exist in entity %s.' %
                (name, source_key))
        if dst.isnull().any():
            raise ValueError(
                'Some destination entities in relation %s do not exist in entity %s.' %
                (name, destination_key))

        srctype = self.entity_pk_to_name[source_key]
        dsttype = self.entity_pk_to_name[destination_key]
        etype = (srctype, name, dsttype)
        self.relation_name_to_etype[name] = etype
        self.edges_per_relation[etype] = (src.cat.codes.values.astype('int64'), dst.cat.codes.values.astype('int64'))
        self.relation_tables[name] = relation_table
        self.relation_src_key[name] = source_key
        self.relation_dst_key[name] = destination_key

    def build(self):
        # Create heterograph
        graph = dgl.heterograph(self.edges_per_relation, self.num_nodes_per_type)
        return graph
