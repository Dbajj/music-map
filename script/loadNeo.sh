#!/bin/bash

systemctl stop neo4j
rm -rf /var/lib/neo4j/data/databases/graph.db/
cd data/
neo4j-admin import --nodes="csv_header/artist_header.csv,csv/artist.csv" --relationships="csv_header/release_header.csv,csv/release.csv" --ignore-missing-nodes=true

chown -R neo4j:neo4j /var/lib/neo4j/
systemctl start neo4j


end="$((SECONDS+60))"
while true; do
    nc -w 2 localhost 7687 && break
    [[ "${SECONDS}" -ge "${end}" ]] && echo 'Error: could not access neo4j server after starting, check if up' && exit 1
    sleep 1
done

echo 'Service running'

cypher-shell -u 'neo4j' -p $NEO4J_PASS 'CREATE INDEX ON :Artist(name);'
cypher-shell -u 'neo4j' -p $NEO4J_PASS 'CREATE INDEX ON :Artist(artistId);'

