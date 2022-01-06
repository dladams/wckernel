# wckernel.py
#
# David Adams
# January 2022
#
# Class to view and create fcl for wirecell TPC field response maps.

import json
import numpy as np

class WcReponseMap:

    def __init__(self, fnam ='data/dunevd-resp-isoc3views.json'):
        with open(fnam) as fin: j = json.load(fin)
        planes = j['FieldResponse']['planes']
        npla = len(planes)
        self.resp = [None]*npla      # Array of of numpy 2D-arrays holding the response for each plane
        print(f"""Plane count is {npla}""")
        for ipla in range(0, npla):
            plane = planes[ipla]
            paths = plane['PlaneResponse']['paths']
            npat = len(paths)
            neles = []
            for ipat in range(0, npat):
                path = paths[ipat]
                elems = path['PathResponse']['current']['array']['elements']
                nele = len(elems)
                neles.append(nele)
            nele1 = min(neles)
            nele2 = max(neles)
            if nele1 == nele2:
                seleMsg =f"""{nele1} elements"""
            else:
                seleMsg =f"""{nele1}-{nele2}) elements"""
            print(f"""  Plane {ipla} has {npat} paths, each with {seleMsg}""")
            self.resp[ipla] = np.zeros((npat, nele2), np.float64)
            for ipat in range(0, npat):
                path = paths[ipat]
                self.resp[ipla][ipat] = path['PathResponse']['current']['array']['elements']
    def __getitem__(self, ipla):
        return self.response(ipla)

    def nplane(self):
        """Return the number of planes."""
        return len(self.resp)

    def response(self, ipla):
        if ipla >= self.nplane(): return None
        return self.resp[ipla]
