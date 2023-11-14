# Mobility Data Warehouse

A data warehouse that integrates mobility data from various sources with corresponding context data such as weather conditions, economics, etc.

## Tech Stack
- Postgresql
- Python
- Pygrametl
- Bonobo

## Data Model
The data warehouse is designed according to Kimball's star schema with main table _trajectory_ as fact connected to dimension tables.
![Trajectory Data Warehouse](https://github.com/drwoj/mobility_data_warehouse/assets/84898707/c8fadb86-85b9-4946-8484-0134cde826f5)

Fact constellation schema would allow more in-depth analysis, but conducted tests have shown that the star schema performs much better and provides sufficient analytic possibilities.

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


