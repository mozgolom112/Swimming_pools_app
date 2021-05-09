-- FUNCTION: public.insert_ticket()

-- DROP FUNCTION public.insert_ticket();

CREATE FUNCTION public.insert_ticket()
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
	BEGIN
		-- Первый этап, создаем тренировочную запись
		type_of_water_ := (SELECT type_of_water FROM public."Swimming_pools" where id = New.id_pool);
		RAISE NOTICE 'Current value of parameter type_of_water_ (%)', type_of_water_;
		INSERT INTO public."Training_sessions"(
			type_of_water) 
			VALUES (type_of_water_) RETURNING id INTO id_training_;

		RAISE NOTICE 'Current value of parameter id_training (%)', id_training_;
		New.id_training := id_training_;
		
		-- Второй этап, обнавляем запись сеанса
		session_id_ := (select id from "Swimming_sessions" where id_pool = New.id_pool and date_and_time = New.date_and_time);
		--RAISE NOTICE 'Current value of parameter comparing (%)', date_and_time = New.date_and_time;
		RAISE NOTICE 'Current value of parameter session_id (%)', session_id_;
		UPDATE "Swimming_sessions" Set entry_tickets = entry_tickets + 1 where id = session_id_;
		
		IF New.type = 2 THEN
			UPDATE "Swimming_sessions" Set discount_tickets = discount_tickets + 1 where id = session_id_;
		END IF;
		workload_ := upd_workload(session_id_);
		RAISE NOTICE 'Current value of parameter workload_ (%)', workload_;
		RETURN NEW;
	END;
$BODY$;

ALTER FUNCTION public.insert_ticket()
    OWNER TO postgres;
