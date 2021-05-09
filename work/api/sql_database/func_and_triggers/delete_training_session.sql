-- FUNCTION: public.delete_training_session(integer)

-- DROP FUNCTION public.delete_training_session(integer);

CREATE OR REPLACE FUNCTION public.delete_training_session(
	training_session_id integer)
    RETURNS integer
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE 
BEGIN

    Update "Tickets" Set id_training = NULL where id_training = training_session_id;
	DELETE FROM "Training_sessions" where id = training_session_id;
	RETURN 0;

END;
$BODY$;

ALTER FUNCTION public.delete_training_session(integer)
    OWNER TO postgres;
