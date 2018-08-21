#!/bin/bash

systemctl stop neo4j
rm -rf /var/lib/neo4j/data/databases/graph.db/
cd data/csv/
neo4j-admin import --nodes="artist-header.csv,artist.csv" --relationships="release-header.csv,release.csv" --ignore-missing-nodes=true

chown -R neo4j:neo4j /var/lib/neo4j/
systemctl start neo4j
