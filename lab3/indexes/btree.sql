CREATE INDEX treeIndex ON public."Readers" using btree (reader_id);

ALTER TABLE public."Readers"
    ADD COLUMN ts_vector1 tsvector;

UPDATE public."Readers"
SET ts_vector1 = to_tsvector(fullname)
WHERE true;




EXPLAIN SELECT * FROM public."Readers"

EXPLAIN ANALYSE SELECT * FROM public."Readers" where reader_id < 100100;