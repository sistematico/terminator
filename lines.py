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


# kt.replace("\r", "\t")

print (" ".join(line.strip() for line in sql1.splitlines() ))

#print("".join(sql1.splitlines()))