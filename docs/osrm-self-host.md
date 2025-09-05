# Self-hosted OSRM

Run an OSRM instance with Australian data.

```bash
# download data
wget https://download.geofabrik.de/australia-oceania/australia-latest.osm.pbf

# extract, partition and customise
docker run -t -v $PWD:/data osrm/osrm-backend osrm-extract -p /opt/car.lua /data/australia-latest.osm.pbf
docker run -t -v $PWD:/data osrm/osrm-backend osrm-partition /data/australia-latest.osrm
docker run -t -v $PWD:/data osrm/osrm-backend osrm-customize /data/australia-latest.osrm

# serve on http://localhost:5000
OSRM_BASE_URL=http://localhost:5000 \
docker run -p 5000:5000 -t -v $PWD:/data osrm/osrm-backend osrm-routed --algorithm mld /data/australia-latest.osrm
```

The application reads the base URL from the `OSRM_BASE_URL` environment variable.
