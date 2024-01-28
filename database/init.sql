CREATE TABLE example_table (
    id serial PRIMARY KEY,
    float_col float,
    int_col int,
    varchar_col varchar(100),
    bool_col bool,
    timestamp_col timestamp,
    jsonb_col jsonb,
    other_col1 text,
    other_col2 text,
    other_col3 text,
    other_col4 text,
    other_col5 text,
    other_col6 text,
    other_col7 text,
    other_col8 text
);

INSERT INTO example_table 
    (float_col, int_col, varchar_col, bool_col, timestamp_col, jsonb_col, other_col1, other_col2, other_col3, other_col4, other_col5, other_col6, other_col7, other_col8)
VALUES
    (1.23, 42, 'Sample 1', true, '2023-01-01 12:00:00', '{"key1": "value1"}', 'Other 1-1', 'Other 1-2', 'Other 1-3', 'Other 1-4', 'Other 1-5', 'Other 1-6', 'Other 1-7', 'Other 1-8'),
    (3.45, 78, 'Sample 2', false, '2023-01-02 15:30:00', '{"key2": "value2"}', 'Other 2-1', 'Other 2-2', 'Other 2-3', 'Other 2-4', 'Other 2-5', 'Other 2-6', 'Other 2-7', 'Other 2-8'),
    (5.67, 105, 'Sample 3', true, '2023-01-03 09:15:00', '{"key3": "value3"}', 'Other 3-1', 'Other 3-2', 'Other 3-3', 'Other 3-4', 'Other 3-5', 'Other 3-6', 'Other 3-7', 'Other 3-8'),
    (8.90, 150, 'Sample 4', false, '2023-01-04 18:45:00', '{"key4": "value4"}', 'Other 4-1', 'Other 4-2', 'Other 4-3', 'Other 4-4', 'Other 4-5', 'Other 4-6', 'Other 4-7', 'Other 4-8'),
    (12.34, 200, 'Sample 5', true, '2023-01-05 14:30:00', '{"key5": "value5"}', 'Other 5-1', 'Other 5-2', 'Other 5-3', 'Other 5-4', 'Other 5-5', 'Other 5-6', 'Other 5-7', 'Other 5-8'),
    (15.67, 250, 'Sample 6', false, '2023-01-06 11:00:00', '{"key6": "value6"}', 'Other 6-1', 'Other 6-2', 'Other 6-3', 'Other 6-4', 'Other 6-5', 'Other 6-6', 'Other 6-7', 'Other 6-8'),
    (18.90, 300, 'Sample 7', true, '2023-01-07 08:30:00', '{"key7": "value7"}', 'Other 7-1', 'Other 7-2', 'Other 7-3', 'Other 7-4', 'Other 7-5', 'Other 7-6', 'Other 7-7', 'Other 7-8'),
    (21.23, 350, 'Sample 8', false, '2023-01-08 17:00:00', '{"key8": "value8"}', 'Other 8-1', 'Other 8-2', 'Other 8-3', 'Other 8-4', 'Other 8-5', 'Other 8-6', 'Other 8-7', 'Other 8-8'),
    (24.56, 400, 'Sample 9', true, '2023-01-09 13:45:00', '{"key9": "value9"}', 'Other 9-1', 'Other 9-2', 'Other 9-3', 'Other 9-4', 'Other 9-5', 'Other 9-6', 'Other 9-7', 'Other 9-8'),
    (27.89, 450, 'Sample 10', false, '2023-01-10 10:15:00', '{"key10": "value10"}', 'Other 10-1', 'Other 10-2', 'Other 10-3', 'Other 10-4', 'Other 10-5', 'Other 10-6', 'Other 10-7', 'Other 10-8'),
    (31.23, 500, 'Sample 11', true, '2023-01-11 07:45:00', '{"key11": "value11"}', 'Other 11-1', 'Other 11-2', 'Other 11-3', 'Other 11-4', 'Other 11-5', 'Other 11-6', 'Other 11-7', 'Other 11-8'),
    (34.56, 550, 'Sample 12', false, '2023-01-12 16:15:00', '{"key12": "value12"}', 'Other 12-1', 'Other 12-2', 'Other 12-3', 'Other 12-4', 'Other 12-5', 'Other 12-6', 'Other 12-7', 'Other 12-8'),
    (37.89, 600, 'Sample 13', true, '2023-01-13 12:00:00', '{"key13": "value13"}', 'Other 13-1', 'Other 13-2', 'Other 13-3', 'Other 13-4', 'Other 13-5', 'Other 13-6', 'Other 13-7', 'Other 13-8'),
    (41.23, 650, 'Sample 14', false, '2023-01-14 09:30:00', '{"key14": "value14"}', 'Other 14-1', 'Other 14-2', 'Other 14-3', 'Other 14-4', 'Other 14-5', 'Other 14-6', 'Other 14-7', 'Other 14-8'),
    (44.56, 700, 'Sample 15', true, '2023-01-15 18:00:00', '{"key15": "value15"}', 'Other 15-1', 'Other 15-2', 'Other 15-3', 'Other 15-4', 'Other 15-5', 'Other 15-6', 'Other 15-7', 'Other 15-8'),
    (47.89, 750, 'Sample 16', false, '2023-01-16 14:45:00', '{"key16": "value16"}', 'Other 16-1', 'Other 16-2', 'Other 16-3', 'Other 16-4', 'Other 16-5', 'Other 16-6', 'Other 16-7', 'Other 16-8'),
    (51.23, 800, 'Sample 17', true, '2023-01-17 11:15:00', '{"key17": "value17"}', 'Other 17-1', 'Other 17-2', 'Other 17-3', 'Other 17-4', 'Other 17-5', 'Other 17-6', 'Other 17-7', 'Other 17-8'),
    (54.56, 850, 'Sample 18', false, '2023-01-18 07:45:00', '{"key18": "value18"}', 'Other 18-1', 'Other 18-2', 'Other 18-3', 'Other 18-4', 'Other 18-5', 'Other 18-6', 'Other 18-7', 'Other 18-8'),
    (57.89, 900, 'Sample 19', true, '2023-01-19 16:15:00', '{"key19": "value19"}', 'Other 19-1', 'Other 19-2', 'Other 19-3', 'Other 19-4', 'Other 19-5', 'Other 19-6', 'Other 19-7', 'Other 19-8'),
    (61.23, 950, 'Sample 20', false, '2023-01-20 12:00:00', '{"key20": "value20"}', 'Other 20-1', 'Other 20-2', 'Other 20-3', 'Other 20-4', 'Other 20-5', 'Other 20-6', 'Other 20-7', 'Other 20-8');

CREATE SCHEMA DJANGO_PG_SCHEMA;
CREATE SCHEMA AIRBYTE_SCHEMA;