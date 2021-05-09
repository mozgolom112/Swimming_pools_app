-- FUNCTION: public.delete_client()

-- DROP FUNCTION public.delete_client();

CREATE FUNCTION public.delete_client()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
DECLARE
		type_of_water_ integer;
		id_training_ integer;
		session_id_ integer;
		workload_ double precision;
		i integer = 0;
		t_row "Tickets"%rowtype;
	BEGIN
		FOR t_row in select * from "Tickets" where id_client = OLD.id LOOP
		id_training_ := t_row.id_training;
		UPDATE "Tickets" Set id_training = NULL where id_training = id_training_;
		Delete from "Training_sessions" where id = id_training_;
		RAISE NOTICE 'delete_client| Current value of parameter i (%)', i;
		RAISE NOTICE 'delete_client| Current value of parameter id_training_ (%)', id_training_;
	END LOOP;
	UPDATE "Tickets" Set id_client = NULL where id_client = Old.id;
	RETURN Old;
	END;
$BODY$;

ALTER FUNCTION public.delete_client()
    OWNER TO postgres;
