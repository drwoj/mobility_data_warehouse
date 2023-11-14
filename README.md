# Mobility Data Warehouse

Data warehouse that integrates mobility data from various sources along with coresponding context data such as: weather condition, economics etc.

## Tech Stack
- Postgresql
- Python
- Pygrametl
- Bonobo

## Data Model
Data warehouse is designed according to Kimball's star schema main table _trajectory_ as fact which is connected to dimension tables.
It was considered to use fact constellation schema, but conducted tests has shown that the star schema performs much better.
![performance comparison](https://github.com/drwoj/mobility_data_warehouse/assets/84898707/e761ece3-df6c-4c9b-bf14-5e8d07e6b9f2)


## Data Sources
### mobility data:
- Geolife GPS trajectory dataset: https://www.microsoft.com/en-us/download/details.aspx?id=52367
- Hannover trajectories: https://data.uni-hannover.de/dataset/single-user-trajectory-collection-for-the-region-of-hannover

### context data:
- weather: https://www.ncei.noaa.gov/cdo-web/datasets
- economics: https://databank.worldbank.org/source/world-development-indicators
- fuel prices for China: https://info.ceicdata.com/
- fuel prices for Hannover: https://www.destatis.de/EN/Home/_node.html


