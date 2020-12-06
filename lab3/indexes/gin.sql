ALTER TABLE public."Readers"
    ADD COLUMN ts_vector tsvector;

UPDATE public."Readers"
SET ts_vector = to_tsvector(fullname)
WHERE true;

CREATE INDEX ginIndex ON public."Readers" USING gin (ts_vector);




EXPLAIN SELECT * FROM public."Readers"

EXPLAIN SELECT * FROM public."Readers" WHERE to_tsquery('c') @@ ts_vector;