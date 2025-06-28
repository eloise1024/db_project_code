-- Create tables
CREATE TABLE "user" (
    user_id VARCHAR PRIMARY KEY CHECK (user_id ~ '^u[0-9]{6}$'),
    name VARCHAR,
    number CHAR(11),
    register_time DATE
);

CREATE TABLE home (
    home_id VARCHAR PRIMARY KEY CHECK (home_id ~ '^home[0-9]{6}$'),
    area_sqm FLOAT,
    address TEXT
);

CREATE TABLE user_home_relation (
    user_id VARCHAR,
    home_id VARCHAR,
    relation TEXT CHECK (relation IN ('member', 'admin')),
    PRIMARY KEY (user_id, home_id),
    FOREIGN KEY (user_id) REFERENCES "user"(user_id),
    FOREIGN KEY (home_id) REFERENCES home(home_id)
);

CREATE TABLE device (
    device_id VARCHAR PRIMARY KEY CHECK (device_id ~ '^d[0-9]{6}$'),
    device_type VARCHAR,
    name VARCHAR,
    home_id VARCHAR,
    room_name TEXT,
    install_time DATE,
    FOREIGN KEY (home_id) REFERENCES home(home_id)
);

CREATE TABLE device_usage_log (
    usage_id VARCHAR PRIMARY KEY CHECK (usage_id ~ '^r[0-9]{6}$'),
    device_id VARCHAR,
    start_time TIMESTAMPTZ,
    duration_seconds NUMERIC(6,2),
    FOREIGN KEY (device_id) REFERENCES device(device_id)
);

CREATE TABLE device_feedback (
    feedback_id VARCHAR PRIMARY KEY CHECK (feedback_id ~ '^f[0-9]{6}$'),
    device_id VARCHAR,
    user_id VARCHAR,
    submit_time TIMESTAMPTZ,
    problem_description TEXT,
    resolved BOOLEAN,
    FOREIGN KEY (device_id) REFERENCES device(device_id),
    FOREIGN KEY (user_id) REFERENCES "user"(user_id)
);

CREATE TABLE security_event (
    event_id VARCHAR PRIMARY KEY CHECK (event_id ~ '^e[0-9]{6}$'),
    home_id VARCHAR,
    event_time TIMESTAMPTZ,
    device_id VARCHAR,
    FOREIGN KEY (home_id) REFERENCES home(home_id),
    FOREIGN KEY (device_id) REFERENCES device(device_id)
);