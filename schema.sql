CREATE TABLE applications (
    app_name TEXT PRIMARY KEY,
    current_version INTEGER,
    repo_owner TEXT NOT NULL,
    repo_name TEXT NOT NULL,
    branch TEXT
);

CREATE TABLE application_versions (
    app_name TEXT NOT NULL,
    version INTEGER NOT NULL,
    installed_at INTEGER,
    commit TEXT,
    path TEXT,
    is_downloaded BOOLEAN,
    PRIMARY KEY (app_name, version)
);

CREATE TABLE scripts (
    app_name TEXT PRIMARY KEY,
    path TEXT NOT NULL
);

CREATE TABLE triggers (
    app_name TEXT NOT NULL,
    -- One of 'ALWAYS', 'COMMIT', 'TIMER'.
    type TEXT NOT NULL,
    -- Update period in seconds.
    update_period INTEGER,
    PRIMARY KEY (app_name, type)
);
