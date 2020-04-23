from graphviz import Digraph
import datetime
from time import strftime

# Input 1
in1 = {'list1': [{'duration': datetime.timedelta(seconds=774, microseconds=701000),
            'finish': datetime.datetime(2020, 4, 8, 23, 35, 8, 224000),
            'idle_time': datetime.timedelta(0),
            'kb_time': datetime.timedelta(seconds=8, microseconds=181000),
            'mouse_time': datetime.timedelta(seconds=6, microseconds=147000),
            'name': 'pycharm64.exe',
            'icon_path': '/Users/odrac/OneDrive/Pictures/PyCharm.png',
            'start': datetime.datetime(2020, 4, 8, 23, 22, 13, 523000)},
           {'duration': datetime.timedelta(seconds=28, microseconds=142000),
            'finish': datetime.datetime(2020, 4, 8, 23, 35, 36, 370000),
            'idle_time': datetime.timedelta(0),
            'kb_time': datetime.timedelta(seconds=8, microseconds=181000),
            'mouse_time': datetime.timedelta(seconds=6, microseconds=147000),
            'name': 'pycharm64.exe',
            'icon_path': '/Users/odrac/OneDrive/Pictures/PyCharm.png',
            'start': datetime.datetime(2020, 4, 8, 23, 35, 8, 228000)},
           {'duration': datetime.timedelta(seconds=6, microseconds=229000),
            'finish': datetime.datetime(2020, 4, 8, 23, 37, 57, 462000),
            'idle_time': datetime.timedelta(0),
            'kb_time': datetime.timedelta(0),
            'mouse_time': datetime.timedelta(seconds=6, microseconds=229000),
            'name': 'firefox.exe',
            'icon_path': '/Users/odrac/OneDrive/Pictures/FireFox.png',
            'start': datetime.datetime(2020, 4, 8, 23, 37, 51, 233000)}],
 'list2': [{'duration': datetime.timedelta(seconds=8, microseconds=345000),
            'finish': datetime.datetime(2020, 4, 8, 23, 37, 59, 582000),
            'idle_time': datetime.timedelta(0),
            'kb_time': datetime.timedelta(seconds=8, microseconds=181000),
            'mouse_time': datetime.timedelta(seconds=6, microseconds=147000),
            'name': 'pycharm64.exe',
            'icon_path': '/Users/odrac/OneDrive/Pictures/PyCharm.png',
            'start': datetime.datetime(2020, 4, 8, 23, 37, 51, 237000)}]}

#  Input 2
in2 = {'wifi_info': '     agrCtlRSSI: -29\n     agrExtRSSI: 0\n    agrCtlNoise: -91\n    agrExtNoise: 0\n          state: running\n        op mode: station \n     lastTxRate: 144\n        maxRate: 144\nlastAssocStatus: 0\n    802.11 auth: open\n      link auth: wpa2-psk\n          BSSID: da:52:c9:5a:5c:c0\n           SSID: iPhone\n            MCS: 15\n        channel: 6\n',
'username': 'atagowani',
'homedir': '/Users/atagowani',
'alt_homedir': 'Atas-MacBook-Pro.local',
'hostname': 'Atas-MacBook-Pro.local',
'ip_address': '172.20.10.2',
'mac_address': '0xf21898076563',
'formatted_mac_address': '0xf21898076563',
'hostname_by_address': None}


def generateDiagram(app_info, user_info):

  g = Digraph('G', filename='bpd')
  g.attr(rankdir='TB', size='8,5')
  fontname = "Helvetica"

  # NOTE: the subgraph name needs to begin with 'cluster' (all lowercase)
  #       so that Graphviz recognizes it as a special cluster subgraph

  username = user_info["username"]
  mac_addy = user_info["mac_address"]
  ip_addy = user_info["ip_address"]
  date = str(datetime.date.today())

  with g.subgraph(name='cluster_0') as c:
      c.attr(color='grey11', fontname=fontname)
      c.attr('node', shape='box', style='filled', color="lightskyblue1", fontname=fontname, margin=".15")
      # c.node_attr['fixedsize'] = 'false'
      # c.attr('node', shape='box')
      edges =  []

      for list in app_info:
        for app in app_info[list]:
          # print(app["name"])
          # print("===")

          dummyStart= app["start"]
          startTime= dummyStart.strftime("%r")

          dummyFinish= app["finish"]
          finishTime= dummyFinish.strftime("%r")



          path= app["icon_path"]

          c.node(str(app["start"]).replace(':','') + app["name"], '''<<TABLE border="0">
          <TR><TD fixedsize="true" width="55" height="50" bgcolor="transparent"><IMG SRC="'''+ path + '''"/></TD>
          <TD align="center" valign="middle">'''+ app["name"] + '''<BR/><BR/>''' + startTime + ' - ' + finishTime + '''<BR/><BR/>Duration<BR/>'''+ str(app["duration"]) + '''</TD></TR>
          <TR><TD></TD></TR></TABLE>>''', width='5', height='1.5')
          #c.node(str(app["start"]).replace(':','') + app["name"], label=app["name"] + str(app["duration"]))
        # print(len(app_info[list]))
        for i in range(len(app_info[list]) - 1):
          edges.append((str(app_info[list][i]["start"]).replace(':','') + app_info[list][i]["name"], str(app_info[list][i+1]["start"]).replace(':','') + app_info[list][i+1]["name"]))

      #print(edges)
      c.edges(edges)

      # Node Definitions
      # c.node('Cisco WebEx', label="Cisco Webex \n\n 8:00 AM - 10:23 AM \n\n Duration \n 2 hours")
      # c.node('PowerShell', label="PowerShell \n\n 10:23 AM - 11:00 AM \n\n Duration \n 37 Minutes")
      # c.node('Microsoft Word',  label="Microsoft Word \n\n 11:00 AM - 1:00 PM \n\n Duration \n 2 hours")
      # c.attr('node', fixedsize="true", width="5", height="1.5")
      # c.node('Google Chrome', label="Google Chrome \n\n 8:00 AM - 5:00 PM \n\n Duration \n 9 hours")

      # Node Edges
      # c.edges([('Cisco WebEx', 'PowerShell'), ('PowerShell', 'Microsoft Word')])
      c.attr(label="User= " + username + " | MAC= " + mac_addy + " | IP= " + ip_addy + " | " + date)



  # with g.subgraph(name='cluster_1') as c:
  #     c.attr(color='blue')
  #     c.node_attr['style'] = 'filled'
  #     c.node_attr['shape'] = 'box'
  #     c.edges([('b0', 'b1'), ('b1', 'b2'), ('b2', 'b3')])
  #     c.attr(label='swimlane #2')

  g.view()

generateDiagram(in1, in2)
