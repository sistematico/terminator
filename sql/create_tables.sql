PRAGMA foreign_keys = ON;
        
CREATE TABLE IF NOT EXISTS grupos(
  id integer PRIMARY KEY, 
  gid integer UNIQUE, 
  nome text, 
  flags integer DEFAULT 111
);

CREATE TABLE IF NOT EXISTS usuarios(
  id integer PRIMARY KEY,
  uid integer,
  gid integer,
  apelido text,
  nome text,
  warnings integer NOT NULL DEFAULT 0,
  likes integer NOT NULL DEFAULT 0,
  FOREIGN KEY(gid) REFERENCES grupos (gid)
);

CREATE UNIQUE INDEX IF NOT EXISTS usuarios_idx ON usuarios (uid,gid);     