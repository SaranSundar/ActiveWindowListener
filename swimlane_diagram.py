from graphviz import Digraph

g = Digraph('G', filename='bpd')
g.attr(rankdir='LR', size='8,5')

# NOTE: the subgraph name needs to begin with 'cluster' (all lowercase)
#       so that Graphviz recognizes it as a special cluster subgraph

username = "saran"
mac_addy = "ac:de:48:00:11:22"
ip_addy = "192.168.1.67"

with g.subgraph(name='cluster_0') as c:
    c.attr(color='blue')
    c.node_attr['shape'] = 'box'
    # c.node_attr['fixedsize'] = 'false'
    c.node_attr.update(style='filled')
    c.edges([('Chrome \n\n Timestamp \n 2020-03-04 \n 08hour 23min 55sec \n\n Duration \n 2 hours', 'PowerShell \n\n Timestamp \n 2020-03-04 \n 10hour 23min 55sec \n\n Duration \n 2 hours'), ('PowerShell \n\n Timestamp \n 2020-03-04 \n 10hour 23min 55sec \n\n Duration \n 2 hours', 'Word')])
    c.attr(label="username= " + username + " | MAC= " + mac_addy + " | IP= " + ip_addy)

# with g.subgraph(name='cluster_1') as c:
#     c.attr(color='blue')
#     c.node_attr['style'] = 'filled'
#     c.node_attr['shape'] = 'box'
#     c.edges([('b0', 'b1'), ('b1', 'b2'), ('b2', 'b3')])
#     c.attr(label='swimlane #2')

g.view()