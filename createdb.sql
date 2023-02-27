create table urls(
    id integer primary key,
    url varchar(255),
    name varchar(255)
);

create table prices(
    id integer primary key,
    drug_id integer,
    drug_name varchar(255),
    store_name varchar(255),
    price float
);

create table gui_settings(
    id integer primary key AUTOINCREMENT,
    excel_path varchar(255),
    parser_type int,
    streams_count int,
    is_proxy int
);

create table proxies(
    id integer primary key AUTOINCREMENT,
    ip varchar(50),
    port varchar(50),
    proxy_type varchar(50)
);

create table user_agents(
    id integer primary key AUTOINCREMENT,
    user_agent varchar(255)
);