CREATE TABLE tables
(
    table_id Uint64,
    description Utf8,
    cnt Uint64,
    PRIMARY KEY (table_id)
);

CREATE TABLE reservations
(
    phone String,
    description Utf8,
    table_id Uint64,
    cnt Uint64,
    dt DateTime,
    PRIMARY KEY (dt, phone),
);

COMMIT;
