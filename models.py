from crypto_password import hash_password


class User:

    def __init__(self, username='', password='', salt=''):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)
    
    @property
    def id(self):
        
        return self._id
    
    @property
    def hashed_password(self):
        
        return self._hashed_password
    
    def set_password(self, password, salt=''):
        self._hashed_password = hash_password(password, salt)
    
    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)
    
    def save_to_db(self, cursor):
        
        if self._id == -1:
            sql = """
                INSERT INTO users(username, hashed_password)
                VALUES(%s, %s) RETURNING id;
            """
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
        
            return True
        
        else:
            sql = """
                UPDATE users SET username=%s, hashed_password=%s
                WHERE id=%s;
            """
            values = (self.username, self.hashed_password, self._id)
            cursor.execute(sql, values)
        
            return True
    
    @staticmethod
    def load_user_by_username(cursor, username):
        sql = """
            SELECT id, username, hashed_password FROM users
            WHERE username=%s;
        """
        cursor.execute(sql, (username,))
        data = cursor.fetchone()
        
        if data:
            user_id, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = user_id
            loaded_user._hashed_password = hashed_password
        
            return loaded_user
        
        else:
        
            return None
        
    @staticmethod
    def load_user_by_id(cursor, user_id):
        sql = """
            SELECT id, username, hashed_password FROM users
            WHERE id=%s;
        """
        cursor.execute(sql, (user_id,))
        data = cursor.fetchone()
        
        if data:
            user_id, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = user_id
            loaded_user._hashed_password = hashed_password
        
            return loaded_user
        
        else:
        
            return None
    
    @staticmethod
    def load_all_users(cursor):
        sql = """
            SELECT id, username, hashed_password FROM users;
        """
        users = []
        cursor.execute(sql)
        
        for row in cursor.fetchall():
            user_id, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = user_id
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        
        return users
    
    def delete(self, cursor):
        sql = "DELETE FROM users WHERE id=%s"
        cursor.execute(sql, (self._id,))
        self._id = -1
        
        return True


class Message:

    def __init__(self, from_id, to_id, text):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self._date_of_created = None
    
    @property
    def id(self):

        return self._id
    
    @property
    def date_of_created(self):

        return self._date_of_created
    
    @staticmethod
    def load_all_messages(cursor, to_id=None):
        
        if to_id:
            sql = """
                SELECT id, from_id, to_id, text, date_of_created
                FROM messages WHERE to_id=%s;
            """
            cursor.execute(sql, (to_id,))
        
        else:
            sql = """
                SELECT id, from_id, to_id, text, date_of_created
                FROM messages;
            """
            cursor.execute(sql)
        
        messages = []

        for row in cursor.fetchall():
            message_id, from_id, to_id, text, date_of_created = row
            loaded_message = Message(from_id, to_id, text)
            loaded_message._id = message_id
            loaded_message._date_of_created = date_of_created
            messages.append(loaded_message)
        
        return messages
    
    def save_to_db(self, cursor):

        if self._id == -1:
            sql = """
                INSERT INTO messages(from_id, to_id, text)
                VALUES(%s, %s, %s) RETURNING id, date_of_created;
            """
            values = (self.from_id, self.to_id, self.text)
            cursor.execute(sql, values)
            self._id, self._date_of_created = cursor.fetchone()
        
            return True
        
        else:
            sql = """
                UPDATE messages SET from_id=%s, to_id=%s, text=%s
                WHERE id=%s;
            """
            values = (self.from_id, self.to_id, self.text, self._id)
            cursor.execute(sql, values)
        
            return True