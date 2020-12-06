CREATE OR REPLACE FUNCTION InsertReader()
    returns trigger
    language plpgsql
AS
$$
BEGIN
    IF NEW.age > 50 THEN
        UPDATE public."Subscriptions" SET type= ' (old)' WHERE "Subscriptions".subscription_id = NEW.subscription_id;
    ELSE
        UPDATE public."Subscriptions" SET type= ' (young)' WHERE "Subscriptions".subscription_id = NEW.subscription_id;
    END IF;
    return NEW;
END;
$$;

CREATE TRIGGER setSubscriptionType
    INSERT
    ON public."Readers"
    FOR EACH ROW
EXECUTE PROCEDURE InsertReader();

DROP TRIGGER setSubscriptionType on public."Readers";