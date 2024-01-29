

# DE Zoomcamp Module 1  - Homework 1

### Freanu Peria

## Preparing for the Questions

A. Loading Green Taxi Data
Docker-compose had complications (did not run at first, and when I got to fix it, tables were empty and running the script would return an error)
so what I did was I just ran the previous two containers and ingest the data


```
docker run -it \
-e POSTGRES_USER="root" \
-e POSTGRES_PASSWORD="root" \
-e POSTGRES_DB="ny_taxi" \
-v dtc_postgres_volume_local:/var/lib/postgresql/data \
-p 5432:5432 \
--network=pg-network \
--name pg-database \
postgres:13


docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pg-admin \
  dpage/pgadmin4


  running ingest script

URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"

python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=green_taxi_data \
  --url=${URL}


(check ingest_data.py in this repo, it was modified for the green taxi data)
```

B. Loading Taxi Lookup Data
I don't have much time left to modify the containers and scripts, so what I did was

- I simply read the data from within a new notebook and used pandas for manipulating data

- Manually imported the lookup data in pgadmin and used SQL

-----------------------------------------------------------------------------

## My Solutions to the Answers

1. I just ran
```
docker --help
docker build --help
docker run --help
```

2. I just ran
```
docker run -it python:3.9 bash

pip list
```

3. I used pandas
```
import pandas as pd

green_taxi_df = pd.read_csv(r"C:\code\de-zoomcamp\week_1\data\green_tripdata_2019-09.csv", low_memory=False)

green_taxi_df[
    (green_taxi_df['lpep_pickup_datetime'] > '2019-09-18')
      &
    (green_taxi_df['lpep_dropoff_datetime'] < '2019-09-19')
].shape
```

4. I used the pgadmin (this is when I decided to ingest the data for the green taxi data and import the lookup data)
```

SELECT DISTINCT DATE(lpep_pickup_datetime) 
FROM green_taxi_data
WHERE trip_distance = (SELECT MAX(trip_distance) FROM green_taxi_data);
```


5. For this part, I got confused because in github homework it said that the sum of the three boroughs should be more than 50000 but there are some boroughs that could get more than 50k.
so I checked the link of the homework and saw that the question only asked for the top three, so that's why I ended up with my answer
```
SELECT "b"."borough", sum(total_amount) as total

FROM GREEN_TAXI_DATA a 
	INNER JOIN TAXI_ZONE b
		ON "a"."PULocationID" = b."locationid"

WHERE (DATE(LPEP_PICKUP_DATETIME) = '2019-09-18' 
AND DATE(LPEP_DROPOFF_DATETIME) = '2019-09-18')
GROUP BY "b"."borough"
ORDER BY total dESC
```

6. first I joined green taxi data and taxi zones by pickup location id so that I can filter it by zone "Astoria"
and the date to sept 2019. Then I joined again to select the details of the dropoff zone.
I contained it in a subquery

then I selected the max tip amount and zone, then grouping it by the zone and lastly ordering it by tip.
the first one is the JFK airport
```
SELECT max(tip_amount) as tip_amount, zone FROM
(

select a.*, c.*
FROM GREEN_TAXI_DATA a 
	INNER JOIN TAXI_ZONE b
		ON "a"."PULocationID" = b."locationid"
	INNER JOIN TAXI_ZONE c
		ON "a"."DOLocationID" = c."locationid"
		
where lower("b"."zone") = 'astoria'
and extract(year from LPEP_PICKUP_DATETIME) = 2019
and extract(month from LPEP_PICKUP_DATETIME) = 9

) as x

group by zone
order by tip_amount desc;

```


7. I wasn't so sure where I should run the terraform commands because there are two folders on the course repo directory which we were asked to download.
I updated the tf files in `terraform_basic` and `terraform_with_variables`

I just cd into the `terraform_basic` folder and ran the terraform commands

then I ran the commands as instructed in the readme in the folder

I pasted the output of terraform apply in the homework form, it is also in `terraform apply output.txt` .


