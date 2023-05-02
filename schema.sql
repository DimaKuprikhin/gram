CREATE TABLE repositories (
    app_name TEXT PRIMARY KEY,
    repo_owner TEXT NOT NULL,
    repo_name TEXT NOT NULL,
    path TEXT NOT NULL
);

CREATE TABLE scripts (
    app_name TEXT PRIMARY KEY,
    path TEXT NOT NULL
);

CREATE TABLE triggers (
    app_name TEXT PRIMARY KEY,
    -- One of 'ALWAYS', 'COMMIT', 'TIMER'.
    type TEXT NOT NULL,
    -- NULL for COMMIT, 'Nd Nh Nm' for TIMER.
    value TEXT,
    -- Commit hash for COMMIT, timepoint for TIMER.
    currently_at TEXT
);
