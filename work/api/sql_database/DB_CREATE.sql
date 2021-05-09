CREATE TABLE "Clients" (
	"id" serial NOT NULL,
	"name" VARCHAR(200) NOT NULL,
	"surname" VARCHAR(200) NOT NULL,
	"patronymic_name" VARCHAR(200),
	"birth" DATE,
	"date_registration" DATE,
	"phone" VARCHAR(255) NOT NULL UNIQUE,
	CONSTRAINT "Clients_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Training_sessions" (
	"id" serial NOT NULL,
	"duration" TIME NOT NULL,
	"swam_distance" integer NOT NULL,
	"heart_rate" integer,
	"spO2" integer,
	"crawl" integer,
	"backstroke" integer,
	"breaststroke" integer,
	"butterfly" integer,
	"type_of_water" integer DEFAULT '0',
	"swolf" integer,
	"kilocalories" integer,
	CONSTRAINT "Training_sessions_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Tickets" (
	"id" serial NOT NULL,
	"id_client" integer,
	"id_training" integer,
	"id_pool" integer NOT NULL,
	"date_and_time" DATETIME NOT NULL,
	"ticket_type" integer NOT NULL,
	CONSTRAINT "Tickets_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Types_of_water" (
	"type" serial NOT NULL,
	"description" VARCHAR(255) NOT NULL,
	"capacity_per_line" integer NOT NULL DEFAULT '10',
	CONSTRAINT "Types_of_water_pk" PRIMARY KEY ("type")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Swimming_pools" (
	"id" serial NOT NULL,
	"lines" integer NOT NULL,
	"location" integer NOT NULL,
	"type_of_water" integer NOT NULL,
	"capacity" integer NOT NULL DEFAULT '10',
	"monetary_policy" integer NOT NULL DEFAULT '10',
	CONSTRAINT "Swimming_pools_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Pools_locations" (
	"id" serial NOT NULL,
	"address" VARCHAR(255) NOT NULL,
	"city" integer NOT NULL,
	CONSTRAINT "Pools_locations_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Cities" (
	"id" serial NOT NULL,
	"city" VARCHAR(255) NOT NULL UNIQUE,
	CONSTRAINT "Cities_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Swimming_sessions" (
	"id" serial NOT NULL,
	"id_pool" integer NOT NULL,
	"entry_tickets" integer NOT NULL,
	"discount_tickets" integer NOT NULL DEFAULT '0',
	"workload" FLOAT NOT NULL DEFAULT '0',
	"date_and_time" DATETIME NOT NULL,
	CONSTRAINT "Swimming_sessions_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Daily_earnings" (
	"date" DATE NOT NULL,
	"id_pool" integer NOT NULL,
	"clients" integer NOT NULL,
	"workload" integer NOT NULL,
	"proceeds" FLOAT NOT NULL,
	"monetary_policy" integer NOT NULL,
	"discount_clients" integer NOT NULL
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Monetary_policies" (
	"id" serial NOT NULL,
	"ticket_price" integer NOT NULL,
	"preferential_discount" FLOAT NOT NULL,
	"date_of_adoption" DATE NOT NULL,
	CONSTRAINT "Monetary_policies_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Ticket_types" (
	"type" serial NOT NULL,
	"description" serial(255) NOT NULL,
	CONSTRAINT "Ticket_types_pk" PRIMARY KEY ("type")
) WITH (
  OIDS=FALSE
);




ALTER TABLE "Training_sessions" ADD CONSTRAINT "Training_sessions_fk0" FOREIGN KEY ("type_of_water") REFERENCES "Types_of_water"("type");

ALTER TABLE "Tickets" ADD CONSTRAINT "Tickets_fk0" FOREIGN KEY ("id_client") REFERENCES "Clients"("id");
ALTER TABLE "Tickets" ADD CONSTRAINT "Tickets_fk1" FOREIGN KEY ("id_training") REFERENCES "Training_sessions"("id");
ALTER TABLE "Tickets" ADD CONSTRAINT "Tickets_fk2" FOREIGN KEY ("id_pool") REFERENCES "Swimming_pools"("id");
ALTER TABLE "Tickets" ADD CONSTRAINT "Tickets_fk3" FOREIGN KEY ("ticket_type") REFERENCES "Ticket_types"("type");


ALTER TABLE "Swimming_pools" ADD CONSTRAINT "Swimming_pools_fk0" FOREIGN KEY ("location") REFERENCES "Pools_locations"("id");
ALTER TABLE "Swimming_pools" ADD CONSTRAINT "Swimming_pools_fk1" FOREIGN KEY ("type_of_water") REFERENCES "Types_of_water"("type");
ALTER TABLE "Swimming_pools" ADD CONSTRAINT "Swimming_pools_fk2" FOREIGN KEY ("monetary_policy") REFERENCES "Monetary_policies"("id");

ALTER TABLE "Pools_locations" ADD CONSTRAINT "Pools_locations_fk0" FOREIGN KEY ("city") REFERENCES "Cities"("id");


ALTER TABLE "Swimming_sessions" ADD CONSTRAINT "Swimming_sessions_fk0" FOREIGN KEY ("id_pool") REFERENCES "Swimming_pools"("id");

ALTER TABLE "Daily_earnings" ADD CONSTRAINT "Daily_earnings_fk0" FOREIGN KEY ("id_pool") REFERENCES "Swimming_pools"("id");
ALTER TABLE "Daily_earnings" ADD CONSTRAINT "Daily_earnings_fk1" FOREIGN KEY ("monetary_policy") REFERENCES "Monetary_policies"("id");



