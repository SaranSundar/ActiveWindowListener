from graphviz import Digraph
import os

# print(os.path.abspath(os.getcwd()))
g = Digraph('G', filename='bpd')
g.attr(rankdir='TB', size='8,5')
fontname = "Helvetica"

# NOTE: the subgraph name needs to begin with 'cluster' (all lowercase)
#       so that Graphviz recognizes it as a special cluster subgraph

username = "saran"
mac_addy = "ac:de:48:00:11:22"
ip_addy = "192.168.1.67"
date = "03/04/2020"
path="/Users/odrac/OneDrive/Pictures/Webex.png"
appname= "Cisco Webex"

with g.subgraph(name='cluster_0', graph_attr={'newrank': 'same'}) as c:
    c.attr(color='grey11', fontname=fontname)
    c.attr('node', shape='box', style='filled', color="lightskyblue1", fontname=fontname, margin=".15")
    # c.node_attr['fixedsize'] = 'false'
    # c.attr('node', shape='box')

    # Node Definitions
    c.node('Cisco WebEx', '''<<TABLE border="0">
    <TR><TD fixedsize="true" width="55" height="50" bgcolor="transparent"><IMG SRC="'''+ path + '''"/></TD>
    <TD align="center" valign="middle">Cisco Webex<BR/><BR/>8:00 AM - 10:23 AM<BR/><BR/>Duration<BR/>2 hours</TD></TR>
    <TR><TD></TD></TR></TABLE>>''', width='5', height='1.5')

    c.node('PowerShell', '''<<TABLE border="0">
    <TR><TD fixedsize="true" width="55" height="50" bgcolor="transparent"><IMG SRC="/Users/odrac/OneDrive/Pictures/Powershell.png"/></TD>
    <TD align="center" valign="middle">PowerShell<BR/><BR/>10:23 AM - 11:00 AM<BR/><BR/>Duration<BR/>37 Minutes</TD></TR>
    <TR><TD></TD></TR></TABLE>>''', width='5', height='1.5')

    c.node('Microsoft Word', '''<<TABLE border="0">
    <TR><TD fixedsize="true" width="55" height="50" bgcolor="transparent"><IMG SRC="/Users/odrac/OneDrive/Pictures/Word.png"/></TD>
    <TD align="center" valign="middle">Microsoft Word<BR/><BR/>11:00 AM - 1:00 PM<BR/><BR/>Duration<BR/>2 hours</TD></TR>
    <TR><TD></TD></TR></TABLE>>''', width='5', height='1.5')

    c.node('Google Chrome', '''<<TABLE border="0">
    <TR><TD fixedsize="true" width="55" height="50" bgcolor="transparent"><IMG SRC="/Users/odrac/OneDrive/Pictures/Chrome.png"/></TD>
    <TD align="center" valign="middle">Google Chrome<BR/><BR/>8:00 AM - 5:00 PM<BR/><BR/>Duration<BR/>9 hours</TD></TR>
    <TR><TD></TD></TR></TABLE>>''', width='5', height='1.5')

    c.node('JAVA', '''<<TABLE border="0">
    <TR><TD fixedsize="true" width="55" height="50" bgcolor="transparent"><IMG SRC="/Users/odrac/OneDrive/Pictures/Word.png"/></TD>
    <TD align="center" valign="middle">JAVA<BR/><BR/>11:00 AM - 1:00 PM<BR/><BR/>Duration<BR/>2 hours</TD></TR>
    <TR><TD></TD></TR></TABLE>>''', width='5', height='1.5')

    c.node('MobaXterm', '''<<TABLE border="0">
    <TR><TD fixedsize="true" width="55" height="50" bgcolor="transparent"><IMG SRC="/Users/odrac/OneDrive/Pictures/Chrome.png"/></TD>
    <TD align="center" valign="middle">MobaXterm<BR/><BR/>8:00 AM - 5:00 PM<BR/><BR/>Duration<BR/>9 hours</TD></TR>
    <TR><TD></TD></TR></TABLE>>''', width='5', height='1.5')

    #c.node('PowerPoint', '''<<TABLE border="0">
    # <TR><TD fixedsize="true" width="55" height="50" bgcolor="transparent"><IMG SRC="/Users/odrac/OneDrive/Pictures/Chrome.png"/></TD>
    #<TD align="center" valign="middle">Google Chrome<BR/><BR/>8:00 AM - 5:00 PM<BR/><BR/>Duration<BR/>9 hours</TD></TR>
    #<TR><TD></TD></TR></TABLE>>''', width='5', height='5')



    # Node Edges
    c.edges([('Cisco WebEx', 'PowerShell'), ('PowerShell', 'Microsoft Word'), ('JAVA', 'MobaXterm')])
    c.edge_attr.update(minlen='1')
    c.attr(label="User= " + username + " | MAC= " + mac_addy + " | IP= " + ip_addy + " | " + date)

    #with g.subgraph(name='subs', graph_attr={'rank': 'same'}) as d:
        #d.attr(color='grey11', fontname=fontname)
        #d.attr('node', shape='box', style='filled', color="lightskyblue1", fontname=fontname, margin=".15")
        #d.edge_attr.update(constraint='false')
        #d.node('Google Chrome')
        #d.node('PowerShell')


# with g.subgraph(name='cluster_1') as c:
#     c.attr(color='blue')
#     c.node_attr['style'] = 'filled'
#     c.node_attr['shape'] = 'box'
#     c.edges([('b0', 'b1'), ('b1', 'b2'), ('b2', 'b3')])
#     c.attr(label='swimlane #2')

g.view()
