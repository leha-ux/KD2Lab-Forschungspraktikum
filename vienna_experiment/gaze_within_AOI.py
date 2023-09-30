from shapely.geometry import Polygon, Point, MultiPoint


#Creates shapes from coordinates 
def set_AOI(AOI):
    dict_polygons = {}
    for key, value in AOI.items():
        dict_polygons.update({key : (MultiPoint(value).convex_hull)})
    return dict_polygons


#Decide whether gaze is within shape
def is_in_polygon(shape, x_coordinate, y_coordinate, buffer=10) -> int:
    if shape.intersects(Point(x_coordinate, y_coordinate).buffer(buffer)):
        return 1
    else: 
        return 0

#Calculates average for gaze data
#Expects structure like AOI = {"AOI1" : [[0, 1], [1,1], [1, 0], [0,0]], "AOI2" ....}
#gaze_data = [[0,0], [10,23], ...]
def average_aoi(AOI : dict, gaze_data : list) -> dict:
    average_gaze = {}
    for key, value in set_AOI(AOI).items(): 
        average_gaze.update({key : sum(is_in_polygon(value, gaze[0], gaze[1]) for gaze in gaze_data) / len(gaze_data)})
    return average_gaze


