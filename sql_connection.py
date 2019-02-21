from item import Item
import sqlite3
import os
import sys


class ConnectionManager:
    """
    This class encapsulates all SQL logic and methods
    """

    def __init__(self):
        """
        creates a connection to the database
        """

        # create .db file based on directory where called script is running
        # the .db file will be created if it does not exist
        abs_path = os.path.abspath(os.path.dirname(sys.argv[0]))

        try:
            self.conn = sqlite3.connect(os.path.join(abs_path, "url.db"))

        except sqlite3.Error as e:
            print(e)

    def create_table(self):
        """
        Creates the necessary table to store URL information.
        The table has a unique item name, a url related to that item, its price, and its coupon.
        :return: True or False depending on the status of creation
        """
        sql_stmt = """CREATE TABLE IF NOT EXISTS url_table (
                    item_name VARCHAR(256) PRIMARY KEY,
                    url VARCHAR(256),
                    price VARCHAR(256),
                    coupon VARCHAR(256)
                    );
                    """

        try:
            c = self.conn.cursor()
            c.execute(sql_stmt)

        except sqlite3.Error as e:
            print(e)
            return False

        finally:
            # commit the changes so that they are saved
            self.conn.commit()

        return True

    def upsert_item(self, item):
        """
        Creates a row in the url_table.
        Updates the values by deleting the row if the item name exists
        :param item: An item object
        :return: The status of the creation
        """

        sql_stmt = """ REPLACE INTO url_table(item_name, url, price, coupon)
                        VALUES(?, ?, ?, ?);
                    """

        try:
            cur = self.conn.cursor()
            # pass in a tuple of values for prepared stmt
            cur.execute(sql_stmt, (item.item_name, item.url, item.price, item.coupon))
            return True

        except sqlite3.Error as e:
            print(e)
            return False

        finally:
            # commit the changes so that they are saved
            self.conn.commit()

    def delete_item(self, item):
        """
        Delete a row in the url_table.
        :param item: An item object
        :return: The status of the creation
        """

        sql_stmt = """ DELETE FROM url_table WHERE item_name = :item_name;
                    """

        try:
            cur = self.conn.cursor()
            # pass in a tuple of values for prepared stmt
            cur.execute(sql_stmt, {"item_name": item.item_name})
            return True

        except sqlite3.Error as e:
            print(e)
            return False

        finally:
            # commit the changes so that they are saved
            self.conn.commit()

    def close(self):
        """
        Closes the connection to the database
        :return: None
        """
        self.conn.close()


if __name__ == "__main__":
    test_item = Item("lol", "test_url3", "test_price2", "test_coupon2")

    conn = ConnectionManager()
    conn.upsert_item(test_item)
    conn.close()
