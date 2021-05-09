-- FUNCTION: public.culc_daily_earnings(integer, date)

-- DROP FUNCTION public.culc_daily_earnings(integer, date);

CREATE OR REPLACE FUNCTION public.culc_daily_earnings(
	pool_id integer,
	count_date date)
    RETURNS integer
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE 
    clients_ integer = 0; 
	discount_clients_ integer = 0;
	i integer = 0;
	workload_ double precision = 0;
    capacity_ integer = 0;
	proceeds_ double precision = 0;
	monetary_policy_ integer;
	full_price_ integer;
	discount_ double precision;
	t_row "Swimming_sessions"%rowtype;
BEGIN
  	FOR t_row in select * from "Swimming_sessions" where id_pool = pool_id and date_and_time::date = count_date LOOP
		clients_ := clients_ +  t_row.entry_tickets;
		discount_clients_ := discount_clients_ + t_row.discount_tickets;
		workload_ := workload_ + t_row.workload;
		i := i + 1;
		RAISE NOTICE 'culc_daily_earnings| Current value of parameter i (%)', i;
	END LOOP;
	
	RAISE NOTICE 'culc_daily_earnings| Current value of parameter clients_ (%)', clients_;
	RAISE NOTICE 'culc_daily_earnings| Current value of parameter discount_clients_ (%)', discount_clients_;
	RAISE NOTICE 'culc_daily_earnings| Current value of parameter workload_ (%)', workload_;
	
	monetary_policy_ := (select monetary_policy from "Swimming_pools" where id = pool_id);
	discount_ := (select preferential_discount from "Monetary_policies" where id = monetary_policy_);
	full_price_ := (select ticket_price from "Monetary_policies" where id = monetary_policy_);
	RAISE NOTICE 'culc_daily_earnings| Current value of parameter full_price_ (%)', full_price_;
	RAISE NOTICE 'culc_daily_earnings| Current value of parameter discount_ (%)', discount_;
	
	proceeds_ := clients_*full_price_ - discount_clients_*full_price_*discount_;
	RAISE NOTICE 'culc_daily_earnings| Current value of parameter proceeds_ (%)', proceeds_;
	workload_ := (round(workload_::numeric / i, 6)); 
	RAISE NOTICE 'culc_daily_earnings| Current value of parameter workload_ (%)', workload_;
	
	INSERT INTO public."Daily_earnings"(
	date_, id_pool, clients, workload, proceeds, monetary_policy, discount_clients)
	VALUES (count_date, pool_id, clients_, workload_, proceeds_, monetary_policy_, discount_clients_);
	return 0;
END;
$BODY$;

ALTER FUNCTION public.culc_daily_earnings(integer, date)
    OWNER TO postgres;
