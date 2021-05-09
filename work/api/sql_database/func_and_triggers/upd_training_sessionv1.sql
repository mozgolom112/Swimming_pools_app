-- FUNCTION: public.upd_training_session(integer, time without time zone, integer, integer, integer, integer, integer, integer, integer, integer)

-- DROP FUNCTION public.upd_training_session(integer, time without time zone, integer, integer, integer, integer, integer, integer, integer, integer);

CREATE OR REPLACE FUNCTION public.upd_training_session(
	id_train integer,
	duration_ time without time zone,
	heart_rate_ integer,
	spo2_ integer,
	crawl_ integer,
	backstroke_ integer,
	breaststroke_ integer,
	butterfly_ integer,
	swolf_ integer,
	kilocalories_ integer)
    RETURNS integer
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE 
    swam_distance_ integer = 0; 
BEGIN
	swam_distance_ := crawl_ +  backstroke_ + breaststroke_ + butterfly_;
	UPDATE "Training_sessions" Set 
	duration = duration_,
	swam_distance = swam_distance_,
	heart_rate = heart_rate_,
	"spO2" = spO2_,
	crawl = crawl_,
	backstroke = backstroke_,
	breaststroke = breaststroke_,
	butterfly = butterfly_,
	swolf = swolf_,
	kilocalories = kilocalories_
	where id = id_train;
	return 0;
END;
$BODY$;

ALTER FUNCTION public.upd_training_session(integer, time without time zone, integer, integer, integer, integer, integer, integer, integer, integer)
    OWNER TO postgres;
