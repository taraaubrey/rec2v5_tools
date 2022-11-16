import geopandas as gpd
import pandas as pd
from pathlib import Path, PureWindowsPath

riv_path = Path(r"C:\Users\tfo46\OneDrive - University of Canterbury\Tara_PhD\c_PhD\c_Data\a_source\sw_surface_water\REC2_v5\riverlines.shp")

ws_path = Path(r"C:\Users\tfo46\OneDrive - University of Canterbury\Tara_PhD\c_PhD\c_Data\a_source\sw_surface_water\REC2_v5\ws.shp")

out_path = Path(r'C:\Users\tfo46\OneDrive - University of Canterbury\Tara_PhD\c_PhD\c_Data\b_derived\sw_surface_water\sw_pakipaki_watersheds')

#read files
riv_shp = gpd.read_file(riv_path)
ws_shp = gpd.read_file(ws_path)

#starting id
reach_id_i = 213008
#initial upstream list
upstream_list = riv_shp.loc[riv_shp['NextDownID'] == reach_id]['HydroID']

#get all upstream reaches and exit when index is done (max is 20000)
for i in range(20000):
    print(i)
    try:
        reach_id = upstream_list.iloc[i]
        next_upstream = riv_shp.loc[riv_shp['NextDownID'] == reach_id]['HydroID']
        upstream_list = pd.concat([upstream_list, next_upstream])
    except:
        break
    #print(upstream_list)

#subset to upstream riverlines and watersheds
riv_shp_upstream = riv_shp[riv_shp['HydroID'].isin(list(upstream_list))]
ws_shp_upstream = ws_shp[ws_shp['HydroID'].isin(list(upstream_list))]

#save
riv_shp_upstream.to_file(Path(out_path, f'upstream_riv_{reach_id_i}.shp'))
ws_shp_upstream.to_file(Path(out_path, f'upstream_ws_{reach_id_i}.shp'))