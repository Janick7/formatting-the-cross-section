from pyzwcad import APoint, ZwCAD
import win32com.client

acad = win32com.client.Dispatch("ZwCAD.Application")
zcad = ZwCAD()
mosp = acad.ActiveDocument.ModelSpace
# bl = zcad.doc.Blocks

class Modify:
    EntityNames = ['AcDbPolyline', 'AcDbText']
    selModes = ['full', 'part']
    AllDrawItems = [s for s in mosp]
    sequence = []

    def __init__(self):
        self.selTypes = {
            'area': self.areaFilt,
            'all': self.allFilt,
            'layer': self.layerFilt,
            'text': self.textFilt,
            'line': self.lineFilt
            }

    def select(self, *args):
        self.selection_data = args
        return list(filter(self.selTypes[self.selection_data[1]], self.selection_data[0]))

    def areaFilt(self, s):
        points = [APoint(s.InsertionPoint[0], s.InsertionPoint[1])] if self.EntityNames.index(s.EntityName) else [APoint(s.Coordinates[i-1], co) for i, co in enumerate(s.Coordinates) if i % 2 != 0]
        # if self.EntityNames.index(s.EntityName):
        #     points = [APoint(s.InsertionPoint[0], s.InsertionPoint[1])]
        # else:
        #     points = [APoint(s.Coordinates[i-1], co) for i, co in enumerate(s.Coordinates) if i % 2 != 0]

        a = self.selection_data[3]
        b = self.selection_data[4]
        res = []
        for i in range(len(self.sequence)):
            res.extend([p for p in points if ((a[0]+self.sequence[i][0] < p[0]) == (p[0] < b[0]+self.sequence[i][0])) and ((a[1]+self.sequence[i][1] < p[1]) == (p[1] < b[1]+self.sequence[i][1]))])

        if self.selModes.index(self.selection_data[2]): # 'part'
            return len(res) > 0
        else:
            return len(res) == len(points) # 'full'

    def allFilt(self, s):
        return True

    def layerFilt(self, s):
        return self.selection_data[2] == s.Layer

    def textFilt(self, s):
        if len(self.selection_data) == 2:
            return s.EntityName == 'AcDbText'
        elif s.EntityName == 'AcDbText':
            return self.selection_data[2] in s.TextString


    def lineFilt(self, s):
        return s.EntityName == 'AcDbPolyline'
