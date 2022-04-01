CREATE DATABASE postgres WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.utf8';

\connect postgres

CREATE SCHEMA content;

CREATE TABLE content.currency (
    id character varying(3) primary key,
    symbol character varying(1) NOT NULL
);

CREATE TABLE content.account (
    id serial primary key,
    name character varying(255) NOT NULL,
    initial_amount numeric(19,2) NOT NULL,
    currency_id character varying(3) NOT NULL references content.currency(id)
);

CREATE TABLE content.transaction (
    id serial primary key,
    type character varying(10) NOT NULL,
    date date NOT NULL,
    from_amount numeric(19,2),
    to_amount numeric(19,2),
    fee_amount numeric(19,2),
    fee_currency_id character varying(3) references content.currency(id),
    from_account_id bigint references content.account(id),
    from_currency_id character varying(3) references content.currency(id),
    to_account_id bigint references content.account(id),
    to_currency_id character varying(3) references content.currency(id)
);


CREATE VIEW content.assets AS
 SELECT a.id,
    a.name,
    b.amount,
    a.currency_id
   FROM (content.account a
     JOIN ( SELECT c.account_id,
            sum(c.amount) AS amount
           FROM ( SELECT transaction.from_account_id AS account_id,
                    (- sum((transaction.from_amount + COALESCE(transaction.fee_amount, (0)::numeric)))) AS amount
                   FROM content.transaction
                  GROUP BY transaction.from_account_id
                UNION
                 SELECT transaction.to_account_id AS account_id,
                    sum(transaction.to_amount) AS amount
                   FROM content.transaction
                  GROUP BY transaction.to_account_id
                UNION
                 SELECT account.id AS account_id,
                    account.initial_amount AS amount
                   FROM content.account) c
          GROUP BY c.account_id) b ON ((a.id = b.account_id)));


CREATE VIEW content.exchange AS
 SELECT t.id,
    t.date,
    t.from_amount,
    t.from_currency_id,
    t.to_amount,
    t.to_currency_id,
    t.fee_amount,
    t.fee_currency_id,
    ((100.0 * t.fee_amount) / t.from_amount) AS fee_percent,
    (t.from_amount / t.to_amount) AS rate_dir,
    ((t.from_amount + COALESCE(t.fee_amount, (0)::numeric)) / t.to_amount) AS rate_dir_fee,
    (((t.from_currency_id)::text || ' -> '::text) || (t.to_currency_id)::text) AS currencies_dir,
    (t.to_amount / t.from_amount) AS rate_rev,
    (t.to_amount / (t.from_amount + COALESCE(t.fee_amount, (0)::numeric))) AS rate_rev_fee,
    (((t.to_currency_id)::text || ' -> '::text) || (t.from_currency_id)::text) AS currencies_rev
   FROM content.transaction t
  WHERE ((t.from_currency_id)::text <> (t.to_currency_id)::text)
  ORDER BY t.id DESC;


CREATE VIEW content.total AS
 SELECT a.currency_id AS id,
    sum(a.amount) AS amount,
    a.currency_id
   FROM content.assets a
  GROUP BY a.currency_id
  ORDER BY (sum(a.amount)) DESC;

INSERT INTO content.currency VALUES ('RUB', '₽');
INSERT INTO content.currency VALUES ('USD', '$');
INSERT INTO content.currency VALUES ('EUR', '€');
INSERT INTO content.currency VALUES ('AMD', '֏');
