CREATE TABLE admin_prepmetricsdb.friet_ga_sessiondata (
    ga_date DATE,
    source VARCHAR(45),
    medium VARCHAR(45),
    landing_page VARCHAR(255),
    users INT,
    sessions INT,
    pageviews INT,
    bounces INT,
    newUsers INT,
    avgSessionDuration FLOAT(7,4)
);
CREATE TABLE admin_prepmetricsdb.friet_sc_full (
    sc_date DATE,
    query VARCHAR(255),
    landing_page VARCHAR(255),
    device VARCHAR(45),
    country VARCHAR(45),
    impressions INT,
    clicks INT,
    ctr FLOAT(7,4),
    position FLOAT(7,4)
);
CREATE TABLE admin_prepmetricsdb.friet_sc_lp (
    sc_date DATE,
    landing_page VARCHAR(255),
    device VARCHAR(45),
    country VARCHAR(45),
    impressions INT,
    clicks INT,
    ctr FLOAT(7,4),
    position FLOAT(7,4)
);
CREATE TABLE admin_prepmetricsdb.friet_sc_query (
    sc_date DATE,
    device VARCHAR(45),
    country VARCHAR(45),
    impressions INT,
    clicks INT,
    ctr FLOAT(7,4),
    position FLOAT(7,4)
);