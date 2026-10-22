-- Jason Stys: private accounts, immutable policy/evaluation snapshots and independent reviews.
-- Table/column navigation: docs/SOURCE_MAP.md; constraints preserve transactional review invariants.
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS users (
 name TEXT PRIMARY KEY, password_hash TEXT NOT NULL,
 role TEXT NOT NULL CHECK(role IN ('admin','operator','reviewer'))
);
CREATE TABLE IF NOT EXISTS sessions (
 digest TEXT PRIMARY KEY, username TEXT NOT NULL REFERENCES users(name),
 csrf TEXT NOT NULL, expires REAL NOT NULL, created REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS sessions_user ON sessions(username);
CREATE TABLE IF NOT EXISTS attempts (client TEXT PRIMARY KEY, count INTEGER NOT NULL, started REAL NOT NULL);
CREATE TABLE IF NOT EXISTS policies (
 version INTEGER PRIMARY KEY, content TEXT NOT NULL, digest TEXT NOT NULL, actor TEXT NOT NULL, created TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS workspace (id INTEGER PRIMARY KEY CHECK(id=1), active_version INTEGER NOT NULL REFERENCES policies(version), schema_version INTEGER NOT NULL CHECK(schema_version=1));
CREATE TABLE IF NOT EXISTS evaluations (
 id INTEGER PRIMARY KEY, version INTEGER NOT NULL REFERENCES policies(version), creator TEXT NOT NULL REFERENCES users(name),
 operation TEXT NOT NULL, result TEXT NOT NULL, digest TEXT NOT NULL, created TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS reviews (
 evaluation INTEGER PRIMARY KEY REFERENCES evaluations(id), actor TEXT NOT NULL REFERENCES users(name),
 decision TEXT NOT NULL CHECK(decision IN ('acknowledge','reject')), note TEXT NOT NULL, created TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS audit (id INTEGER PRIMARY KEY, at TEXT NOT NULL, actor TEXT NOT NULL, event TEXT NOT NULL, version INTEGER NOT NULL, detail TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS evaluations_creator ON evaluations(creator,id DESC);
CREATE TRIGGER IF NOT EXISTS immutable_policy_update BEFORE UPDATE ON policies BEGIN SELECT RAISE(ABORT,'immutable policy'); END;
CREATE TRIGGER IF NOT EXISTS immutable_policy_delete BEFORE DELETE ON policies BEGIN SELECT RAISE(ABORT,'immutable policy'); END;
CREATE TRIGGER IF NOT EXISTS immutable_evaluation_update BEFORE UPDATE ON evaluations BEGIN SELECT RAISE(ABORT,'immutable evaluation'); END;
CREATE TRIGGER IF NOT EXISTS immutable_evaluation_delete BEFORE DELETE ON evaluations BEGIN SELECT RAISE(ABORT,'immutable evaluation'); END;
CREATE TRIGGER IF NOT EXISTS immutable_review_update BEFORE UPDATE ON reviews BEGIN SELECT RAISE(ABORT,'immutable review'); END;
CREATE TRIGGER IF NOT EXISTS immutable_review_delete BEFORE DELETE ON reviews BEGIN SELECT RAISE(ABORT,'immutable review'); END;
