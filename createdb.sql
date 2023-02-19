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