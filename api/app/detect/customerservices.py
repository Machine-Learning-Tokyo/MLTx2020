from collections import namedtuple
import pandas as pd
from app.detect.geo_info_caller import get_geo_info
from app.detect import camera
import os

GeoCamera = namedtuple('GeoCamera', 'camera address distance duration')

class customerservices:
    def __init__(self, dur_thr=200):
        self.dur_thr = dur_thr * 60
        self.serviceType = "return closest camera based on user input and position"
        file_path = os.path.join(os.getcwd(), "app", "detect", "morerealdata.csv")
        self.database = pd.read_csv(file_path,delimiter=";")
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
            print(v_dur)
            if v_dur <= self.dur_thr:
                geo_cam = GeoCamera(goodTypeCam[i], geo_info.destinations[i], geo_info.distance_texts[i], geo_info.duration_texts[i])
                geo_cams.append(geo_cam)

        return geo_cams

    def findclosestCam(self, goodTypeCam, userPosition):
        dest_coords = [tuple([c.coorX, c.coorY]) for c in goodTypeCam]
        geo_info = get_geo_info(userPosition, dest_coords)
        geo_cams = self.get_geo_cameras(goodTypeCam, geo_info)
        return geo_cams
    
    def returnAllcorrespondingData(self, geo_cameras):
        for geo_cam in geo_cameras:
            self.result = self.result.append(self.database.loc[self.database['camera'] == geo_cam.camera.databaseID], ignore_index = True)
        return self.result, geo_cameras

    def generateRecommandationList(self, results, geocameras):
        # Generate the recommandation list:
        recommandation = results
        recommandation["name"] = ""
        recommandation["distance"] = ""
        recommandation["duration"] = ""
        recommandation["address"] = ""
        
        #print(recommandation)

        for c in geocameras:
            # Get the good index:
            index = recommandation.index[recommandation.camera == c.camera.databaseID]
            # Set the values:
            recommandation.set_value(index,'distance', c.distance)
            recommandation.set_value(index,'duration', c.duration)
            recommandation.set_value(index,'name', c.camera.name)
            recommandation.set_value(index,'address', c.address)
        
        recommandation.set_index('camera', inplace = True)
        recommandation.sort_values(by='waiting', inplace = True)
        #print(recommandation)
        return(recommandation)

    def solve_request(self, Camlist, Ctype, userPosition):
        goodTypeCam = self.getcamIDfromCtype(Camlist, Ctype)

        geo_cameras = self.findclosestCam(goodTypeCam, userPosition)
        results, geocameras = self.returnAllcorrespondingData(geo_cameras)
        recommandation = self.generateRecommandationList(results, geocameras)

        return(recommandation)

