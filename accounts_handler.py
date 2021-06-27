import sqlite3
import datetime
class accounts_handler:
    #DB
    def init_db(self):
        self.conn = sqlite3.connect('sqlite.db')

    def close_db(self):
        self.conn.close()

    #Credentials
    def add_user(self, discord_id, email, password):
        c = self.conn.cursor()
        c.execute("INSERT INTO Accounts VALUES ('" + str(discord_id) + "', '" + email + "', '" + password + "')")
        self.conn.commit()

    def get_credentials(self, discord_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM Accounts WHERE id=?', [discord_id])
        fetch = c.fetchone()
        return {'email': fetch[1], 'password': fetch[2]}

    def get_credentials_blurred(self, discord_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM Accounts WHERE id=?', [discord_id])
        fetch = c.fetchone()
        blur = ""
        for _ in range(len(fetch[2])):
            blur = blur + "\*"
        return {'email': fetch[1], 'blur': blur}

    def check_if_user_exists(self, discord_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM Accounts WHERE id=' + str(discord_id) + '')
        if c.fetchone():
            return True
        else:
            return False
        
    def update_credentials(self, discord_id, new_email, new_password):
        c = self.conn.cursor()
        c.execute('UPDATE Accounts SET email=?, password=? WHERE id=?', [new_email, new_password, discord_id])
        self.conn.commit()
    
    def delete_credentials(self, discord_id):
        c = self.conn.cursor()
        c.execute('DELETE FROM Accounts WHERE id=?', [discord_id])
        self.conn.commit()

    #Meetings
    def register_meeting(self, discord_id, name, link, time):
        c = self.conn.cursor()
        c.execute('INSERT INTO Meets (id,name,link,time) VALUES (?, ?, ?, ?)',(discord_id, name, link, time))
        self.conn.commit()

    def check_if_meeting_exists(self, name, discord_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM Meets WHERE name=? AND id=?', [name, discord_id])
        if c.fetchone():
            return True
        else:
            return False
    
    def update_meeting_link(self, discord_id, name, new_link): #update meeting name with link
        c = self.conn.cursor()
        c.execute('SELECT * FROM Accounts WHERE id=?', [discord_id])
        c.execute('UPDATE Meets SET link=? WHERE name=?', [new_link, name])
        self.conn.commit()

    def update_meeting_name(self, discord_id, new_name, link): #update meeting link with name
        c = self.conn.cursor()
        c.execute('SELECT * FROM Accounts WHERE id=?', [discord_id])
        c.execute('UPDATE Meets SET name=? WHERE link=?', [new_name, link])
        self.conn.commit()

    def update_meeting_time(self, discord_id, time, name): #update meeting link with name ##todoooo
        c = self.conn.cursor()
        c.execute('SELECT * FROM Accounts WHERE id=?', [discord_id])
        c.execute('UPDATE Meets SET time=? WHERE name=?', [time, name])
        self.conn.commit()

    def delete_meeting(self, discord_id, name): #delete meeting with meeting name
        c = self.conn.cursor()
        c.execute('DELETE FROM Meets WHERE id=?, name=?', [discord_id, name])
        self.conn.commit()

    def list_meetings(self, discord_id): #list meetings
        c = self.conn.cursor()
        c.execute('SELECT * FROM Meets WHERE id=?', [discord_id])
        fetch = c.fetchall()
        return fetch

    def create_session(self, discord_id, link, time):
        c = self.conn.cursor()
        c.execute('INSERT INTO Meetings_ongoing (id,link,start_time,time) VALUES (?, ?, ?, ?)',(discord_id, link, datetime.datetime.now(), time))
        self.conn.commit()
        return c.lastrowid #Session_id

    def update_session(self, session_id, channel_id):
        c = self.conn.cursor()
        c.execute('UPDATE Meetings_ongoing SET channel_id=? WHERE session_id=?', [channel_id, session_id])
        self.conn.commit()

    def get_session(self, session_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM Meetings_ongoing WHERE session_id=?', [session_id])
        fetch = c.fetchone()
        return {'discord_id': fetch[0],'session_id': fetch[1],'channel_id': fetch[2],'link': fetch[3],'start_time': fetch[4],'time': fetch[5]}
            
        #fetch = self.c.fetchone()
        #return fetch
        #self.c.execute('SELECT * FROM Meetings_ongoing WHERE channel_id=?', [channel_id])
        #fetchings = self.c.fetchall()
        #for fetch in fetchings:
        #    print(fetch[0])
        #    if fetch[0] == discord_id:
        #        return fetch[1]

#ah = accounts_handler()
#ah.init_db()
#name = "meeting3"
#discord_id = ""
#print(ah.check_if_meeting_exists(name, discord_id))
#ah.close_db()