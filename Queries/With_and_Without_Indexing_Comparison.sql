-- Measure query time without index
SET enable_indexscan = off;
EXPLAIN ANALYZE SELECT * FROM google_play_apps WHERE category = 'Productivity';



-- Measure query time with index
SET enable_indexscan = on;
EXPLAIN ANALYZE SELECT * FROM google_play_apps WHERE category = 'Productivity';