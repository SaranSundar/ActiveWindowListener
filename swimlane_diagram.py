from graphviz import Digraph

g = Digraph('G', filename='bpd')
g.attr(rankdir='LR', size='8,5')
fontname = "Helvetica"

# NOTE: the subgraph name needs to begin with 'cluster' (all lowercase)
#       so that Graphviz recognizes it as a special cluster subgraph

username = "saran"
mac_addy = "ac:de:48:00:11:22"
ip_addy = "192.168.1.67"
date = "03/04/2020"

with g.subgraph(name='cluster_0') as c:
    c.attr(color='grey11', fontname=fontname)
    c.attr('node', shape='box', style='filled', color="lightskyblue1", fontname=fontname, margin=".15")
    # c.node_attr['fixedsize'] = 'false'
    # c.attr('node', shape='box')

    # Node Definitions
    c.node('Cisco WebEx', label="Cisco Webex \n\n 8:00 AM - 10:23 AM \n\n Duration \n 2 hours")
    c.node('PowerShell', label="PowerShell \n\n 10:23 AM - 11:00 AM \n\n Duration \n 37 Minutes")
    c.node('Microsoft Word',  label="Microsoft Word \n\n 11:00 AM - 1:00 PM \n\n Duration \n 2 hours")
    c.attr('node', fixedsize="true", width="5", height="1.5")
    c.node('Google Chrome', label="Google Chrome \n\n 8:00 AM - 5:00 PM \n\n Duration \n 9 hours")

    # Node Edges
    c.edges([('Cisco WebEx', 'PowerShell'), ('PowerShell', 'Microsoft Word')])
    c.attr(label="User= " + username + " | MAC= " + mac_addy + " | IP= " + ip_addy + " | " + date)

# with g.subgraph(name='cluster_1') as c:
#     c.attr(color='blue')
#     c.node_attr['style'] = 'filled'
#     c.node_attr['shape'] = 'box'
#     c.edges([('b0', 'b1'), ('b1', 'b2'), ('b2', 'b3')])
#     c.attr(label='swimlane #2')

g.view()