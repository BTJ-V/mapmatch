from pathlib import Path

from mappymatch import package_root
from mappymatch.constructs.geofence import Geofence
from mappymatch.constructs.trace import Trace
from mappymatch.maps.nx.nx_map import NxMap
from mappymatch.matchers.lcss.lcss import LCSSMatcher

PLOT = True

if PLOT:
    import webbrowser

    from mappymatch.utils.plot import plot_geofence, plot_matches, plot_trace

print("loading trace.")
trace = Trace.from_csv("./directions.csv")

# generate a geofence polygon that surrounds the trace; units are in meters;
# this is used to query OSM for a small map that we can match to
print("building geofence.")
geofence = Geofence.from_trace(trace, padding=100)

# uses osmnx to pull a networkx map from the OSM database
print("pull osm map.")
nx_map = NxMap.from_geofence(geofence)

print("matching .")
matcher = LCSSMatcher(nx_map)

match_result = matcher.match_trace(trace)

if PLOT:
    tmap_file = Path("trace_map.html")
    tmap = plot_trace(trace, plot_geofence(geofence))
    tmap.save(str(tmap_file))
    webbrowser.open(tmap_file.absolute().as_uri())

    mmap_file = Path("matches_map.html")
    mmap = plot_matches(match_result.matches)
    mmap.save(str(mmap_file))
    webbrowser.open(mmap_file.absolute().as_uri())
