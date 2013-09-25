import binascii

from geojson import Feature, FeatureCollection, dumps

from pyproj import transform, Proj

from shapely import wkt

from sqlalchemy import create_engine, event, MetaData
from sqlalchemy.orm import sessionmaker

RD = (
    "+proj=sterea +lat_0=52.15616055555555 +lon_0=5.38763888888889 "
    "+k=0.999908 +x_0=155000 +y_0=463000 +ellps=bessel "
    "+towgs84=565.237,50.0087,465.658,-0.406857,0.350733,-1.87035,4.0812 "
    "+units=m +no_defs"
)

WGS84 = ('+proj=latlong +datum=WGS84')

wgs84_projection = Proj(WGS84)

# TODO: make this accept any spatialite database as command-line argument
engine = create_engine('sqlite:////home/jsmits/Development/projects/3di/'
                       'spatialite/HydroBaseUrban_Texel.sqlite')


@event.listens_for(engine, "connect")
def connect(dbapi_connection, connection_rec):
    dbapi_connection.enable_load_extension(True)

connection = engine.raw_connection().connection
metadata = MetaData(engine)
metadata.reflect()
tables = [table for table in metadata.tables.keys()
          if not table.lower() == table]
session = sessionmaker(bind=engine)()
session.execute("select load_extension('/usr/lib/libspatialite.so')")

for table in tables:
    query = session.execute("SELECT * FROM %s" % table)
    features = []
    for row in query.fetchall():
        pk = row.PK_UID
        try:
            geometry_as_hex = binascii.hexlify(str(row.Geometry))
        except AttributeError:
            print "no Geometry column found in table %s" % table
            break
        geometry_as_wkt = session.execute("SELECT ST_AsText(X'%s')" %
                                          geometry_as_hex).fetchone()[0]
        properties = [(key, row[key]) for key in row.keys()
                      if key not in ['PK_UID', 'Geometry']]
        geometry = wkt.loads(geometry_as_wkt)
        # convert projection (RD) to WGS84
        orig_coords = geometry._get_coords()
        wgs84_coords = []
        for orig_x, orig_y in orig_coords:
            wgs84_x, wgs84_y = transform(Proj(RD), wgs84_projection, orig_x,
                                         orig_y)
            wgs84_coords.append((wgs84_x, wgs84_y))
        geometry._set_coords(wgs84_coords)
        feature = Feature(id=int(pk), geometry=geometry,
                          properties=dict(properties))
        features.append(feature)

    output = dumps(FeatureCollection(features))
    f = open('HydroBaseUrban_Texel__%s.geojson' % table, 'w')
    f.write(output)
    f.close()

if __name__ == '__main__':
    # TODO: implement this properly
    pass
