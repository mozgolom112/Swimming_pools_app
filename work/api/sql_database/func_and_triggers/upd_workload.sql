-- FUNCTION: public.upd_workload(integer)

-- DROP FUNCTION public.upd_workload(integer);

CREATE OR REPLACE FUNCTION public.upd_workload(
	session_id integer)
    RETURNS double precision
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE 
    tickets_ integer; 
	pool_id_ integer;
    capacity_ integer;
	workload_ double precision;
BEGIN
    tickets_ := (select entry_tickets from public."Swimming_sessions" where id = session_id);
	pool_id_ := (select id_pool from public."Swimming_sessions" where id = session_id);
    capacity_ := (select capacity from public."Swimming_pools" where id = pool_id_);
	RAISE NOTICE 'upd_workload| Current value of parameter capacity_ (%)', capacity_;
	RAISE NOTICE 'upd_workload| Current value of parameter tickets_ (%)', tickets_;
	workload_ := (round(tickets_::numeric / capacity_, 4));
	UPDATE "Swimming_sessions" Set workload = workload_ where id = session_id;
	return workload_;
END;
$BODY$;

ALTER FUNCTION public.upd_workload(integer)
    OWNER TO postgres;
