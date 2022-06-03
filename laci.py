from modify import Modify, APoint



c1 = Modify() # Tervezett magasságok
allSelected = list(c1.AllDrawItems)

print(0)
szekvKezd = c1.select(allSelected, 'text', 'Kszelv.    1')
szekvMind = c1.select(allSelected, 'text', 'Kszelv. ')
c1.sequence = [APoint(s.InsertionPoint) - APoint(szekvKezd[0].InsertionPoint) for s in szekvMind]
tervMag = c1.select(allSelected, 'area', 'part', APoint(10.000, 36.845, 0), APoint(287.000, 63.690, 0))
for el in c1.select(tervMag, 'text'):
    el.color = 255

tervKSZ = c1.select(allSelected, 'layer', 'Pen005')
tervKSZ = c1.select(tervKSZ, 'line')
print([t.Coordinates for t in tervKSZ if len(t.Coordinates) > 4])
tervKSZ = [t for t in tervKSZ if len(t.Coordinates) > 4]


