CREATE TABLE cip2010_cip2020 (
    CIP2010Code varchar(7),
    CIP2010Title text,
    Action varchar(40),
    TextChange varchar(5),
    CIP2020Code varchar(7),
    CIP2020Ttitle text
);

CREATE TABLE cip2020_soc2018 (
    CIP2020Code varchar(7),
    CIP2020Title text,
    SOC2018Code varchar(7),
    SOC2018CodeTitle text,
    CIP2020CodeMain char(2),
    CIP2020CodeSubMain char(5)
);

create table bls2020 (
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

CREATE TABLE bls2020description (
    field text,
    description text
);


