from xml.dom import minidom
import osmnx as ox
osm_file = "map.osm"
ouput_file = "map.graphml"

G = ox.graph_from_xml(osm_file, simplify=True) #Dùng hàm graph_from_xml() của osmnx để chuyển tệp map.osm thành một đồ thị mạng đường giao thông
ox.save_graphml(G, ouput_file) #lưu đồ thị ra tệp graphml
print("Done")

def parseXML(output_file): #hàm parseXMl để phân tích tệp XML
    print("Parsing XML")
    xmldoc = minidom.parse(output_file)
    return xmldoc