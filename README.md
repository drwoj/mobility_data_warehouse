# Mobility Data Warehouse

A data warehouse that integrates mobility data from various sources with corresponding context data such as weather conditions, economics, etc.
Main subject are trajectories from Beijing and Hannover.

## Tech Stack
- Postgresql (with PostGIS and MobilityDB)
- Python (mainly GeoPandas)

## Data Model
The data warehouse is designed according to Kimball's star schema with main table _trajectory_ as fact connected to dimension tables.
![Trajectory Data Warehouse](https://github.com/drwoj/mobility_data_warehouse/assets/84898707/4324e255-968d-49d9-81c2-ff016df5fe41)



Fact constellation schema would allow more in-depth analysis, but conducted tests have shown that the star schema performs much better and provides sufficient analytic possibilities.
![performance comparison](https://github.com/drwoj/mobility_data_warehouse/assets/84898707/185a1914-1a5f-4c02-a626-3f690c4531a2)

## Data Sources
### mobility data:
- Geolife GPS trajectory dataset: https://www.microsoft.com/en-us/download/details.aspx?id=52367
- Hannover trajectories: https://data.uni-hannover.de/dataset/single-user-trajectory-collection-for-the-region-of-hannover

### context data:
- weather: https://www.ncei.noaa.gov/cdo-web/datasets
- economics: https://databank.worldbank.org/source/world-development-indicators
- fuel prices for China: https://info.ceicdata.com/
- fuel prices for Hannover: https://www.destatis.de/EN/Home/_node.html

## Visualization
### Interactive map created with Kepler GL:
https://kepler.gl/demo/map?mapUrl=https://dl.dropboxusercontent.com/scl/fi/p7dxmzvgh2vrfdr56n4g7/keplergl_ceekkb3.json?rlkey=2e43abpdj92utej8he0kcsugm&dl=0

### Usage examples:
![trajectory](https://github.com/drwoj/mobility_data_warehouse/assets/84898707/362f5429-7b58-4321-aaa2-ebc2de6f407c)
![district](https://github.com/drwoj/mobility_data_warehouse/assets/84898707/e6a1be72-b337-44c4-89c6-7cd1983e4935)


