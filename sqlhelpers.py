from blockchain import Block, Blockchain


class InvalidTransactionException(Exception):
    pass


class InsufficientFundsException(Exception):
    pass


class Table:
    def __init__(self, mysql, table_name, *args):
        self.mysql       = mysql
        self.table       = table_name
        self.columns     = "(%s)" % ",".join(args)
        self.columnsList = args

        if self._is_new_table(table_name):
            create_data = ",".join("%s varchar(100)" % col for col in self.columnsList)
            cur = self.mysql.connection.cursor()
            cur.execute("CREATE TABLE %s(%s)" % (self.table, create_data))
            cur.close()

    def _is_new_table(self, table_name):
        cur = self.mysql.connection.cursor()
        try:
            cur.execute(
                "SELECT COUNT(*) FROM information_schema.tables "
                "WHERE table_schema = DATABASE() AND table_name = %s",
                [table_name]
            )
            row = cur.fetchone()
            cur.close()
            # DictCursor returns dict, regular returns tuple
            count = list(row.values())[0] if isinstance(row, dict) else row[0]
            return count == 0
        except Exception:
            cur.close()
            return True

    def getall(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM %s" % self.table)
        data = cur.fetchall()
        cur.close()
        return data

    def insert(self, *args):
        data = ",".join('"%s"' % arg for arg in args)
        cur = self.mysql.connection.cursor()
        cur.execute("INSERT INTO %s%s VALUES(%s)" % (self.table, self.columns, data))
        self.mysql.connection.commit()
        cur.close()

    def deleteall(self):
        self.drop()
        self.__init__(self.mysql, self.table, *self.columnsList)

    def drop(self):
        cur = self.mysql.connection.cursor()
        cur.execute("DROP TABLE %s" % self.table)
        cur.close()


def get_blockchain(mysql):
    blockchain     = Blockchain()
    blockchain_sql = Table(mysql, "blockchain", "number", "hash", "previous", "data", "nonce")
    for b in blockchain_sql.getall():
        blockchain.add(Block(int(b['number']), b['previous'], b['data'], int(b['nonce'])))
    return blockchain


def sync_blockchain(mysql, blockchain):
    blockchain_sql = Table(mysql, "blockchain", "number", "hash", "previous", "data", "nonce")
    blockchain_sql.deleteall()
    for block in blockchain.chain:
        blockchain_sql.insert(
            str(block.number), block.hash(), block.previous_hash, block.data, block.nonce
        )
