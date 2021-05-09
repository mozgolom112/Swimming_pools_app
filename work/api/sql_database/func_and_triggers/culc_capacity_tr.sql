-- FUNCTION: public.culc_capacity_tr(integer, integer)

-- DROP FUNCTION public.culc_capacity_tr(integer, integer);

CREATE OR REPLACE FUNCTION public.culc_capacity_tr(
	lines integer,
	type_water_id integer)
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

    lines_ := lines;
    type_of_water_ := type_water_id;
	capacity_per_line_ := (select capacity_per_line from public."Types_of_water" where "type"= type_of_water_);
	
	RETURN lines_ * capacity_per_line_;

END;
$BODY$;

ALTER FUNCTION public.culc_capacity_tr(integer, integer)
    OWNER TO postgres;
