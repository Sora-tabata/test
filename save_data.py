import numpy as np
from calc_traj import CalcTraj
from init import Init
from optimize_traj7 import OptimizeTraj
from optimize_gps import OptimizeGPS
import folium

class SaveData():
    def __init__(self):
        self.groundtruth = CalcTraj().calcGroundTruth(Init().N0, Init().M0)
        #self.orbslam = CalcTraj().calcOrbslam(self.groundtruth, Init().L0)
        #self.opensfm = CalcTraj().calcOpensfm(self.groundtruth, Init().json_file0)
        self.optimized = OptimizeTraj().calcOptimizeTraj()
        #self.optimized_gps = np.array(OptimizeGPS(extract_dist=200).optimizeGPS(self.optimized, 10)[0])
        self.gps_t = Init().gps_t
        self.road_gps = np.array(OptimizeGPS(extract_dist=200).optimizeGPS(self.optimized, 2)[1])

    def saveData_toRyuchi(self):
        #data = np.vstack([self.opensfm[1], self.opensfm[0], self.opensfm[2], self.opensfm[3], self.opensfm[4]]).T
        #print(len(self.optimized[1]))
        #print(len(self.optimized[3][1:]))
        data = np.vstack([self.optimized[1], self.optimized[0], self.optimized[3][:], self.optimized[4][:], self.optimized[5][:]]).T
        np.savetxt("data.csv", data, delimiter=",")

    def saveData_gps(self):
        data = np.vstack([self.optimized_gps.T[0], self.optimized_gps.T[1]]).T
        np.savetxt("optimizedGPS.csv", data, delimiter=",")
        m = folium.Map(location=self.gps_t[0], zoom_start=20)
        for data1, data2 in zip(np.array(self.optimized_gps), self.gps_t):
            folium.Circle(data2.tolist(), radius=0.1, color='black', fill=False).add_to(m)
            folium.Circle(data1.tolist(), radius=0.1, color='magenta', fill=False).add_to(m)
        m
        m.save('output/map_final.html')

    def saveData_toAka(self):
        data = np.vstack([self.road_gps.T[0], self.road_gps.T[1]]).T
        np.savetxt("road_gps.csv", data, delimiter=",")
SaveData().saveData_toAka()