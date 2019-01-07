# GENVASC Recruitement Model Presentation

Presentations to demonstrate the GENVASC recruitment model.

## Pre-requisites

### Normal, Nice, Modern Requirements

Install the requirements using pip:

```bash
pip3 install -r requirements.txt
```

### Basemap

Installing Basemap is a bit more difficult.  I think maybe only the 3rd step is needed, but who knows?

1. First you need to install Geos (I think, probably).  The version in the Basemap instructions does not
work on Ubuntu 18.04, so you have to install the latest version from the [Geos Website](https://trac.osgeo.org/geos/).
You can use the same instructions, but use the latest package instead.
2. Unzip the source code, go into the directory and run the following commands:
```bash
export GEOS_DIR=/usr/local
./configure --prefix=$GEOS_DIR
make; make install
```
3. Run:

```bash
sudo apt install python3-mpltoolkits.basemap
```

To check if it is installed correctly, open a python shell and type:

```python
from mpl_toolkits.basemap import Basemap
```

## Drawing the map

This is based on [this example](http://www.datadependence.com/2016/06/creating-map-visualisations-in-python/)

County boundaries and other location data from data.gov.uk as a [Geoserver shapefile download service](http://maps.communities.gov.uk/geoserver/web/?wicket:bookmarkablePage=:org.geoserver.web.demo.MapPreviewPage)

### Data Queries

- [Counties](http://maps.communities.gov.uk:80/geoserver/dclg_inspire/ows?service=WFS&version=2.0.0&request=GetFeature&typeName=dclg_inspire:English%20Ceremonial%20Counties&outputFormat=shape-zip&srsName=EPSG:4326)
- [Urban Areas](http://maps.communities.gov.uk:80/geoserver/dclg_inspire/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=dclg_inspire:Urban_Settlements_2001_WGS84&maxFeatures=5000&outputFormat=SHAPE-ZIP)
- [Towns](http://maps.communities.gov.uk:80/geoserver/dclg_inspire/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=dclg_inspire:English%20Town%20Centres%202004&maxFeatures=5000&outputFormat=SHAPE-ZIP)

# Theme

[Paletton Theme](http://paletton.com/#uid=31l0u0k4pw002Zk1rKA8KqZeLmi)