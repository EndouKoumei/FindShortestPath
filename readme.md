# Find Shortest Path using A* Algorithm On OpenStreetMap

## 1. Data
* Data has been extracted from [OSM](https://www.openstreetmap.org/).<br>
* Description about data:
  * Data provided by OSM is in __.osm__ format, which is nothing but the XML file.
  * Converted this file to lighter XML _(.graphml)_ file, which can be parsed easily as compared to .osm. [Code](https://github.com/lnvanhuy/FindShortestPath/blob/main/data/transMapgraphml.py) 
  * Used OSMNX for this [OSMNX Documentation](https://osmnx.readthedocs.io/en/stable/osmnx.html#osmnx.core.graph_from_file)

## 2. Algorithm: A*

## 3. UI
* Used [OpenStreetMap](https://www.openstreetmap.org/#map=6/16.11/105.81) to generate data and render the map
* You can click anywhere on the map. The first mouse event recorded will be treated as __Source__ and second will be __Destination__.
* In order to generate output - click anywhere on the map. It will call the [API](https://github.com/lnvanhuy/FindShortestPath/blob/main/src/flaskAPI.py) developed using Flask.
* Path will be displayed by marker with "line" animation.