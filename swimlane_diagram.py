from graphviz import Digraph

g = Digraph('G', filename='bpd')
g.attr(rankdir='LR', size='8,5')

# NOTE: the subgraph name needs to begin with 'cluster' (all lowercase)
#       so that Graphviz recognizes it as a special cluster subgraph

with g.subgraph(name='cluster_0') as c:
    c.attr(color='blue')
    c.node_attr['shape'] = 'box'
    c.node_attr.update(style='filled')
    c.edges([('Chrome', 'PowerShell'), ('PowerShell', 'Word')])
    c.attr(label='swimlane #1')

with g.subgraph(name='cluster_1') as c:
    c.attr(color='blue')
    c.node_attr['style'] = 'filled'
    c.node_attr['shape'] = 'box'
    c.edges([('b0', 'b1'), ('b1', 'b2'), ('b2', 'b3')])
    c.attr(label='swimlane #2')

g.view()