CREATE TABLE IF NOT EXISTS cip2010_cip2020 (
    cip2010code varchar(7),
    cip2010title text,
    action varchar(40),
    textchange varchar(5),
    cip2020code varchar(7),
    cip2020title text
);

CREATE TABLE IF NOT EXISTS  cip2020_soc2018 (
    cip2020code varchar(7),
    cip2020title text,
    soc2018code varchar(7),
    soc2018title text,
);

CREATE TABLE IF NOT EXISTS bls2020 (
    occ_code char(7),
    occ_title text,
    o_group text,
    tot_emp serial,
    emp_prse real,
    h_mean real,
    a_mean bigserial,
    mean_prse real,
    h_pct10 real,
    h_pct25 real,
    h_median real,
    h_pct75 real,
    h_pct90 real,
    a_pct10 real,
    a_pct25 real,
    a_median real,
    a_pct75 real,
    a_pct90 real,
    annual boolean,
    hourly boolean
);

CREATE TABLE IF NOT EXISTS bls2020description (
    field text,
    description text
);
