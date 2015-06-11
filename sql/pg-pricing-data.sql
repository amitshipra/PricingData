--
-- PostgreSQL database dump
--


--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_with_oids = false;

--
-- Name: daily_price; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE daily_price (
    id integer NOT NULL,
    data_vendor_id integer NOT NULL,
    symbol_id integer NOT NULL,
    price_date date NOT NULL,
    open_price numeric NOT NULL,
    high_price numeric NOT NULL,
    low_price numeric NOT NULL,
    close_price numeric NOT NULL,
    created_date timestamp without time zone DEFAULT now() NOT NULL,
    last_updated_date timestamp without time zone DEFAULT now() NOT NULL
);


--
-- Name: daily_price_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE daily_price_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: daily_price_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE daily_price_id_seq OWNED BY daily_price.id;


--
-- Name: data_vendor; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE data_vendor (
    id integer NOT NULL,
    vendor_name text NOT NULL,
    website_url text,
    support_email text,
    created_date timestamp without time zone DEFAULT now() NOT NULL,
    last_updated_date timestamp without time zone DEFAULT now() NOT NULL
);


--
-- Name: data_vendor_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE data_vendor_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: data_vendor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE data_vendor_id_seq OWNED BY data_vendor.id;


--
-- Name: exchange; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE exchange (
    id integer NOT NULL,
    abbrev text NOT NULL,
    exchange_name text NOT NULL,
    city text,
    country text,
    currency text,
    timezone_offset time without time zone,
    created_date timestamp without time zone DEFAULT now() NOT NULL,
    last_updated_date timestamp without time zone DEFAULT now() NOT NULL
);


--
-- Name: exchange_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE exchange_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 99999
    CACHE 1;


--
-- Name: exchange_id_seq1; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE exchange_id_seq1
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: exchange_id_seq1; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE exchange_id_seq1 OWNED BY exchange.id;


--
-- Name: symbol; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE symbol (
    id integer NOT NULL,
    exchange_id integer NOT NULL,
    ticker text NOT NULL,
    instrument text DEFAULT 'EQUITY'::text NOT NULL,
    description text NOT NULL,
    sector text,
    currency text,
    created_date timestamp without time zone DEFAULT now() NOT NULL,
    last_updated_date timestamp without time zone DEFAULT now() NOT NULL
);


--
-- Name: symbol_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE symbol_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: symbol_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE symbol_id_seq OWNED BY symbol.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY daily_price ALTER COLUMN id SET DEFAULT nextval('daily_price_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY data_vendor ALTER COLUMN id SET DEFAULT nextval('data_vendor_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY exchange ALTER COLUMN id SET DEFAULT nextval('exchange_id_seq1'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY symbol ALTER COLUMN id SET DEFAULT nextval('symbol_id_seq'::regclass);


--
-- Name: daily_price_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY daily_price
    ADD CONSTRAINT daily_price_pkey PRIMARY KEY (id);


--
-- Name: data_vendor_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY data_vendor
    ADD CONSTRAINT data_vendor_pkey PRIMARY KEY (id);


--
-- Name: exchange_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY exchange
    ADD CONSTRAINT exchange_pkey PRIMARY KEY (id);


--
-- Name: symbol_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY symbol
    ADD CONSTRAINT symbol_pkey PRIMARY KEY (id);


--
-- Name: daily_price_data_vendor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY daily_price
    ADD CONSTRAINT daily_price_data_vendor_id_fkey FOREIGN KEY (data_vendor_id) REFERENCES data_vendor(id);


--
-- Name: daily_price_symbol_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY daily_price
    ADD CONSTRAINT daily_price_symbol_id_fkey FOREIGN KEY (symbol_id) REFERENCES symbol(id);


--
-- Name: symbol_exchange_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY symbol
    ADD CONSTRAINT symbol_exchange_id_fkey FOREIGN KEY (exchange_id) REFERENCES exchange(id);


--
-- PostgreSQL database dump complete
--

