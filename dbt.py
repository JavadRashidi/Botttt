import mysql.connector
from datetime import datetime, timedelta

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="reminders"
        )
        self.cur = self.conn.cursor()

    ##### Add_user #####
    def add_user(self, id):
        self.cur.execute("SELECT user_id FROM users WHERE user_id=%s", (str(id),))
        result = self.cur.fetchall()

        if not result:
            self.cur.execute("INSERT INTO users (user_id, client, stat) VALUES (%s, %s, %s)", (str(id), '0', "None"))
            self.conn.commit()  

    ##### Update_user #####
    def update_user(self, id, user_chat_friend):
        self.cur.execute("SELECT * FROM users WHERE user_id=%s", (str(user_chat_friend),))
        result = self.cur.fetchone()

        if result and result[1] == '0':
            sql = "UPDATE users SET client=%s WHERE user_id=%s"
            self.cur.execute(sql, (str(id), str(user_chat_friend)))
            self.conn.commit()
            return True

        if result:
            print(f"client value: {result[1]}")
        
        return False
    
    ##### All_user #####
    def all_user(self):
        self.cur.execute("SELECT user_id FROM users")
        users = [j[0] for j in self.cur.fetchall()]
        return users
    
    ##### Check_block #####
    def check_block(self, id):
        self.cur.execute("SELECT stat FROM users WHERE user_id=%s", (str(id),))
        result = self.cur.fetchone()

        if result and result[0] == "None":
            return False
        return True
        
    ##### Add_block #####
    def add_block(self, id):
        self.cur.execute("SELECT * FROM users WHERE user_id=%s", (str(id),))
        result = self.cur.fetchone()

        if result and result[2] == "None":
            sql = "UPDATE users SET stat=%s WHERE user_id=%s"
            self.cur.execute(sql, ("block", str(id)))
            self.conn.commit()
            return True
        
        return False
    
    ##### Remove_block #####
    def remove_block(self, id):
        self.cur.execute("SELECT * FROM users WHERE user_id=%s", (str(id),))
        result = self.cur.fetchone()

        if result and result[2] == "block":
            sql = "UPDATE users SET stat=%s WHERE user_id=%s"
            self.cur.execute(sql, ("None", str(id)))
            self.conn.commit()
            return True
        
        return False
    
    ##### Add_reminder #####
    def add_reminder(self, chat_id, reminder, remind_time):
        self.cur.execute("INSERT INTO reminders (chat_id, reminder, remind_time) VALUES (%s, %s, %s)", 
                         (chat_id, reminder, remind_time))
        self.conn.commit()

    ##### Get_reminders #####
    def get_reminders(self, chat_id):
        self.cur.execute("SELECT reminder, remind_time FROM reminders WHERE chat_id = %s", (chat_id,))
        reminders = self.cur.fetchall()
        return reminders
    
    ##### Delete_reminder #####
    def delete_reminder(self, id):
        self.cur.execute("DELETE FROM reminders WHERE id = %s", (id,))
        self.conn.commit()
    
    ##### Get_due_reminders #####
    def get_due_reminders(self):
        now = datetime.now()
        self.cur.execute("SELECT id, chat_id, reminder, remind_time FROM reminders WHERE remind_time <= %s", (now,))
        reminders = self.cur.fetchall()
        return reminders
    
    ##### Close #####
    def close(self):
        self.cur.close()
        self.conn.close()
