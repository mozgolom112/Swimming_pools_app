-- FUNCTION: public.culc_capacity(integer)

-- DROP FUNCTION public.culc_capacity(integer);

CREATE OR REPLACE FUNCTION public.culc_capacity(
	pool_id integer)
    RETURNS integer
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE 
    lines_ INT; 
    capacity_per_line_ INT;
	type_of_water_ INT;
BEGIN

    lines_ := (select lines from public."Swimming_pools" where "id" = pool_id);
    type_of_water_ := (select type_of_water from public."Swimming_pools" where "id" = pool_id);
	capacity_per_line_ := (select capacity_per_line from public."Types_of_water" where "type"= type_of_water_);
	
	RETURN lines_ * capacity_per_line_;

END;
$BODY$;

ALTER FUNCTION public.culc_capacity(integer)
    OWNER TO postgres;
