sql1 = """
    INSERT OR REPLACE INTO usuarios (uid,gid,warnings) 
    VALUES (
        :uid,
        :gid,
        COALESCE(
            (SELECT warnings FROM usuarios WHERE uid = :uid AND gid = :gid),0
        )+1
    )
    RETURNING warnings;
"""

sql2 = "INSERT OR IGNORE INTO grupos (gid, nome) VALUES (?, ?)"