import matplotlib.pyplot as plt
from networkx import nx
import sys
import csv
import re

def latlong2(filename):
  ret = {}
  with open(filename) as f:
    reader = csv.reader(open(filename))
    for line in reader:
      ret[line[0]] = (int(line[1]), int(line[2]), int(line[3]), int(line[4]))
  return ret

def latlong(filename):
  ret = {}
  with open(filename) as f:
    f.readline()
    for line in f:
      if line.strip() == '':
        continue
      itms = re.split(r'\s+', line.strip(), 9)
      ret[itms[9].replace(' ', '')] = (float(itms[1]), float(itms[2]))
  return ret
    
  
def drawGraph(filename):
  location = latlong('latlong_us.txt')
  g = nx.Graph()
  with open(filename) as f:
    for line in f:
      src, dst = line.split('->')
      tmp = src.split(':')[1].split(',')
      src = tmp[0].replace(' ', '') + ',' + tmp[1].strip()
      tmp = dst.split(':')[1].split(',')
      dst = tmp[0].strip().replace(' ', '') + ',' + tmp[1].strip().split()[0]
      g.add_edge(src, dst)
  print len(g.nodes())
  print len(g.edges())
	  
  pos = {}
  cnt = 0
  for node in g.nodes():
    cnt += 1
    inx = None
    if location.has_key(node):
      inx = node
    else:
      for key in location.keys():
        addr = node.split(',')
        if (addr[0] in key and addr[1] in key):
          inx = key
    if not inx:
      print node
      print "%d/%d" % (cnt, len(g.nodes()))
      raise
    pos[node] = (180-location[inx][1], location[inx][0])
      
  #pos=nx.graphviz_layout(g,prog="fdp")
  #pos=nx.spring_layout(g)
  plt.figure(figsize=(12,8))
  #plt.axis('off')
  plt.xticks([]), plt.yticks([])
  nx.draw_networkx_nodes(g, pos = pos, node_color = 'red', node_size = 30, with_labels=False)
  nx.draw_networkx_edges(g,pos,alpha=0.4)
  plt.axis('equal')
  plt.show()

if __name__ == '__main__':
  #if len(sys.argv) != 2:
  #  print("1 argument needed")
  #  exit()
  #drawGraph(sys.argv[1])
  drawGraph('edges2')
  #latlong('latlong.csv')
