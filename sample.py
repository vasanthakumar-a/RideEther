import gmplot

lat = [10.969644, 10.969644,10.90020]
lng = [77.008981, 77.008981,77.08772]
gmapOne = gmplot.GoogleMapPlotter(10.969644, 77.008981,15)
gmapOne.scatter(lat,lng,'red',size=50,marker=False)
gmapOne.plot(lat,lng,'blue',edge_width=2.5)
gmapOne.draw('sample.html')