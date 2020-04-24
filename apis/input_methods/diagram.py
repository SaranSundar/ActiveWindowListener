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

  with g.subgraph(name='cluster_0', graph_attr={'bgcolor': 'lightcyan4', 'penwidth': '3', 'pencolor': 'navy'}) as c:
      c.attr(color='grey11', fontname=fontname, fontcolor='white')
      c.attr('node', shape='box', style='filled', color="gold", fontname=fontname, margin=".15")

      edges =  []

      for list in app_info:
        for app in app_info[list]:
          # print(app["name"])
          # print("===")

          dummyStart= app["start"]
          startTime= dummyStart.strftime("%I:%M %p")

          dummyFinish= app["finish"]
          finishTime= dummyFinish.strftime("%I:%M %p")

          # Obtains the duration in hours, minutes and seconds format
          dummyDuration= app["duration"]
          total=dummyDuration.seconds
          hours, remainder = divmod(total, 3600)
          minutes, seconds = divmod(remainder, 60)

          # This piece of code would obtain just microseconds if needed/wanted
          #total2=dummyDuration.microseconds
          #hours, remainder = divmod(total, 3600000000)
          #minutes, rem = divmod(remainder, 60000000)
          #seconds, microseconds = divmod(rem, 1000000)

          # If, else if statmenets that will print out values that aren't 0 time
          if hours == 0:
              if minutes == 0:
                  finalDuration = ('%s secs' % (seconds))
              else:
                  finalDuration=('%s mins %s secs' % (minutes, seconds))
          elif minutes == 0 and hours != 0:
              finalDuration=('%s hrs %s secs' % (hours, seconds))
          else:
              finalDuration=('%s hrs %s mins %s secs %s msecs' % (hours, minutes, seconds))

          path= app["icon_path"]

          # Creates the node displaying the app name, start time to end time, and duration
          # along with the app's icon
          c.node(str(app["start"]).replace(':','') + app["name"], '''<<TABLE border="0">
          <TR><TD fixedsize="true" width="55" height="50" bgcolor="transparent"><IMG SRC="'''+ path + '''"/></TD>
          <TD align="center" valign="middle">'''+ app["name"] + '''<BR/><BR/>''' + startTime + ' - ' + finishTime + '''<BR/><BR/>Duration<BR/>'''+ finalDuration + '''</TD></TR>
          <TR><TD></TD></TR></TABLE>>''', width='5', height='1.5')

        # print(len(app_info[list]))
        for i in range(len(app_info[list]) - 1):
          edges.append((str(app_info[list][i]["start"]).replace(':','') + app_info[list][i]["name"], str(app_info[list][i+1]["start"]).replace(':','') + app_info[list][i+1]["name"]))

      # Changes the color of the arrows to red
      c.edge_attr.update(color='red')
      c.edges(edges)

      c.attr(label="User= " + username + " | MAC= " + mac_addy + " | IP= " + ip_addy + " | " + date)

  g.view()

generateDiagram(in1, in2)
