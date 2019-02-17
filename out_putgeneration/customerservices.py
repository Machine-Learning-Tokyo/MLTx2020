from collections import namedtuple
import pandas as pd
from geo_info_caller import get_geo_info

GeoCamera = namedtuple('GeoCamera', 'camera address distance duration')

class customerservices:
    def __init__(self, dur_thr=200):
        self.dur_thr = dur_thr * 60
        self.serviceType = "return closest camera based on user input and position"
        self.database = pd.read_csv('morerealdata.csv',delimiter=";")
        self.result = pd.DataFrame()

    def getcamIDfromCtype(self, Camlist, type):
        goodTypeCam = []
        for cam in Camlist:
            if(cam.Ctype == type ):
                goodTypeCam.append(cam)
        return(goodTypeCam)

    def get_geo_cameras(self, goodTypeCam, geo_info):
        geo_cams = []
        for i, v_dur in enumerate(geo_info.duration_values):
            if v_dur <= self.dur_thr:
                geo_cam = GeoCamera(goodTypeCam[i], geo_info.destinations[i], geo_info.distance_texts[i], geo_info.duration_texts[i])
                geo_cams.append(geo_cam)
        return geo_cams

    def findclosestCam(self, goodTypeCam, userPosition):
        dest_coords = [tuple([c.coorX, c.coorY]) for c in goodTypeCam]
        geo_info = get_geo_info(userPosition, dest_coords)
    
    def returnAllcorrespondingData(self, geo_cameras):
        for geo_cam in geo_cameras:
            self.result = self.result.append(self.database.loc[self.database['camera'] == geo_cam.camera.databaseID], ignore_index = True)
        return self.result

    def solve_request(self, Camlist, Ctype, userPosition):
        goodTypeCam = self.getcamIDfromCtype(Camlist, Ctype)
        geo_cameras = self.findclosestCam(goodTypeCam, userPosition)
        return(self.returnAllcorrespondingData(geo_cameras))
