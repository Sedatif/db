CREATE OR REPLACE FUNCTION afterUpdateSubscription()
    returns trigger
    language plpgsql
AS
$$
DECLARE
    readers cursor is select *
                      from public."Readers"
                      where subscription_id = NEW.subscription_id;
BEGIN
    FOR _reader IN readers
        LOOP
            UPDATE public."Readers"
            SET fullname = NEW.type 
            WHERE reader_id = _reader.reader_id;
        end loop;
    return NEW;
END ;
$$;

CREATE TRIGGER insertType
    AFTER UPDATE
    ON public."Subscriptions"
    FOR EACH ROW
EXECUTE PROCEDURE afterUpdateSubscription();

DROP TRIGGER insertPosition ON department;

select * from public."Readers";

update public."Subscriptions" set type = 'casacsc' where subscription_id = 6;