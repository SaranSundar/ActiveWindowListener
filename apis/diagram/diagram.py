from graphviz import Digraph
import datetime

# Input 1
in1 = {'list1': [{'duration': datetime.timedelta(seconds=774, microseconds=701000),
            'finish': datetime.datetime(2020, 4, 8, 23, 35, 8, 224000),
            'idle_time': datetime.timedelta(0),
            'kb_time': datetime.timedelta(seconds=8, microseconds=181000),
            'mouse_time': datetime.timedelta(seconds=6, microseconds=147000),
            'name': 'pycharm64.exe',
            'start': datetime.datetime(2020, 4, 8, 23, 22, 13, 523000)},
           {'duration': datetime.timedelta(seconds=28, microseconds=142000),
            'finish': datetime.datetime(2020, 4, 8, 23, 35, 36, 370000),
            'idle_time': datetime.timedelta(0),
            'kb_time': datetime.timedelta(seconds=8, microseconds=181000),
            'mouse_time': datetime.timedelta(seconds=6, microseconds=147000),
            'name': 'pycharm64.exe',
            'start': datetime.datetime(2020, 4, 8, 23, 35, 8, 228000)},
           {'duration': datetime.timedelta(seconds=6, microseconds=229000),
            'finish': datetime.datetime(2020, 4, 8, 23, 37, 57, 462000),
            'idle_time': datetime.timedelta(0),
            'kb_time': datetime.timedelta(0),
            'mouse_time': datetime.timedelta(seconds=6, microseconds=229000),
            'name': 'firefox.exe',
            'start': datetime.datetime(2020, 4, 8, 23, 37, 51, 233000)}],
 'list2': [{'duration': datetime.timedelta(seconds=8, microseconds=345000),
            'finish': datetime.datetime(2020, 4, 8, 23, 37, 59, 582000),
            'idle_time': datetime.timedelta(0),
            'kb_time': datetime.timedelta(seconds=8, microseconds=181000),
            'mouse_time': datetime.timedelta(seconds=6, microseconds=147000),
            'name': 'pycharm64.exe',
            'start': datetime.datetime(2020, 4, 8, 23, 37, 51, 237000)}]}

#  Input 2
in2 = "nothing"
# Wifi Info: ['The Wireless AutoConfig Service (wlansvc) is not running.\n']
# Ethernet Info: ['\n', 'Ethernet \n', 'Type: Dedicated \n', 'Administrative state: Enabled \n', 'Connect state: Connected \n', '\n']
# Ethernet Connection: Connected             
# Username: Nikhil Gupta
# Home Directory: C:\Users\Nikhil Gupta
# Alt Hostname: DESKTOP-UGO1A4I
# Hostname: DESKTOP-UGO1A4I
# IP Address: 169.254.79.192
# MAC Address: 0x6245b4f758cc
# MAC Address: 0x6245b4f758cc
# Formatted MAC address: 62:45:b4:f7:58:cc
# Hostname by Address: ('DESKTOP-UGO1A4I', [], ['fe80::3ce1:199d:a45d:4fc0'])
# {'wifi_info': None, 'username': 'Nikhil Gupta', 'homedir': 'C:\\Users\\Nikhil Gupta', 'alt_homedir': 'DESKTOP-UGO1A4I', 'hostname': 'DESKTOP-UGO1A4I', 'ip_address': '169.254.79.192', 'mac_address': '0x6245b4f758cc', 'formatted_mac_address': '0x6245b4f758cc', 'hostname_by_address': ('DESKTOP-UGO1A4I', [], ['fe80::3ce1:199d:a45d:4fc0'])}


def generateDiagram(app_info, user_info):

  g = Digraph('G', filename='bpd')
  g.attr(rankdir='TB', size='8,5')
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

      for app in app_info:
        c.node(app.name, label=app.name + app.duration.hours)

      # Node Definitions
      # c.node('Cisco WebEx', label="Cisco Webex \n\n 8:00 AM - 10:23 AM \n\n Duration \n 2 hours")
      # c.node('PowerShell', label="PowerShell \n\n 10:23 AM - 11:00 AM \n\n Duration \n 37 Minutes")
      # c.node('Microsoft Word',  label="Microsoft Word \n\n 11:00 AM - 1:00 PM \n\n Duration \n 2 hours")
      # c.attr('node', fixedsize="true", width="5", height="1.5")
      # c.node('Google Chrome', label="Google Chrome \n\n 8:00 AM - 5:00 PM \n\n Duration \n 9 hours")

      # Node Edges
      # c.edges([('Cisco WebEx', 'PowerShell'), ('PowerShell', 'Microsoft Word')])
      # c.attr(label="User= " + username + " | MAC= " + mac_addy + " | IP= " + ip_addy + " | " + date)

      

  # with g.subgraph(name='cluster_1') as c:
  #     c.attr(color='blue')
  #     c.node_attr['style'] = 'filled'
  #     c.node_attr['shape'] = 'box'
  #     c.edges([('b0', 'b1'), ('b1', 'b2'), ('b2', 'b3')])
  #     c.attr(label='swimlane #2')

  g.view()

generateDiagram(in1, in2)