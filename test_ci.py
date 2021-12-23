import unittest
import servermain as tested_app
import json 
import random

username_random 

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        path_config = "config_test.json"
        with open(path_config,"r",encoding="utf8") as conf :
            self.config_test = json.loads(conf.read())
        tested_app.app.config['TESTING'] = True
        self.app = tested_app.app.test_client()

    def test_login_pass(self): #login ผ่าน
        
        sent = {"username": self.config_test["login_pass"]["username"], "password": self.config_test["login_pass"]["password"]}
        r = self.app.post('/login',
                          data=sent)
        self.assertEqual(r.json,None)
    
    def test_login_fail(self): #login ไม่ผ่าน
        sent = {"username": self.config_test["login_fail"]["username"], "password":self.config_test["login_fail"]["password"]}   
        r = self.app.post('/login',
                          data=sent)
        self.assertEqual(r.json['code'],401)

    def test_register1(self): #สมัครสมาชิกสำเร็จ
      
        User = = random.randint(500,100000000) #random USER ID
        num = int(self.config_test["register_pass1"]["username"].split('members')[1])
        username_num = str(num+user)
        username = 'members'+username_num
        global username_random = username
        self.config_test["register_pass1"]["username"] = username
        with open("config_test.json", 'w') as f:
            json.dump(self.config_test, f)
        sent = {"username":username_random, "password": self.config_test["register_pass1"]["password"],
        "conpassword":self.config_test["register_pass1"]["conpassword"],"firstname":self.config_test["register_pass1"]["firstname"],
              "lastname":self.config_test["register_pass1"]["lastname"],"gender":self.config_test["register_pass1"]["gender"],
              "email":self.config_test["register_pass1"]["email"]}   
        r = self.app.post('/register',
                          data=sent)
        self.assertEqual(r.json['title'],'สมัครสมาชิกสำเร็จ')
    
    def test_register2(self): #รหัสผ่านต้องมากกว่า 8 ตัวขึ้นไป
        
        sent = {"username":self.config_test["register_pass2"]["username"], "password": self.config_test["register_pass2"]["password"],
        "conpassword":self.config_test["register_pass2"]["conpassword"],"firstname":self.config_test["register_pass2"]["firstname"],
              "lastname":self.config_test["register_pass2"]["lastname"],"gender":self.config_test["register_pass2"]["gender"],
              "email":self.config_test["register_pass2"]["email"]}    
        r = self.app.post('/register',
                          data=sent)
        self.assertEqual(r.json['title'],'รหัสผ่านต้องมากกว่า 8 ตัวขึ้นไป')

    def test_register3(self): #ชื่อผู้ใช้นี้มีในระบบแล้ว
        sent = {"username":self.config_test["register_pass3"]["username"], "password": self.config_test["register_pass3"]["password"],
        "conpassword":self.config_test["register_pass3"]["conpassword"],"firstname":self.config_test["register_pass3"]["firstname"],
              "lastname":self.config_test["register_pass3"]["lastname"],"gender":self.config_test["register_pass3"]["gender"],
              "email":self.config_test["register_pass3"]["email"]} 
        r = self.app.post('/register',
                          data=sent)
        self.assertEqual(r.json['title'],'ชื่อผู้ใช้นี้มีในระบบแล้ว')

    def test_register4(self): #รหัสผ่านไม่ตรงกัน
        sent = {"username":self.config_test["register_pass4"]["username"], "password": self.config_test["register_pass4"]["password"],
        "conpassword":self.config_test["register_pass4"]["conpassword"],"firstname":self.config_test["register_pass4"]["firstname"],
              "lastname":self.config_test["register_pass4"]["lastname"],"gender":self.config_test["register_pass4"]["gender"],
              "email":self.config_test["register_pass4"]["email"]}    
        r = self.app.post('/register',
                          data=sent)
        self.assertEqual(r.json['title'],'รหัสผ่านไม่ตรงกัน')

    def test_register5(self):  #ข้อมูลการสมัครไม่ครบ
        sent = {"username":self.config_test["register_pass5"]["username"], "password": self.config_test["register_pass5"]["password"],
        "conpassword":self.config_test["register_pass5"]["conpassword"],"firstname":self.config_test["register_pass5"]["firstname"],
              "lastname":self.config_test["register_pass5"]["lastname"],"gender":self.config_test["register_pass5"]["gender"],
              "email":self.config_test["register_pass5"]["email"]}    
        r = self.app.post('/register',
                          data=sent)
        self.assertEqual(r.json['title'],'ข้อมูลการสมัครไม่ครบ')

    def test_get_select_hotel(self):

        r = self.app.get('/selectroom')

        self.assertEqual(r.status_code,200)

    def test_logout_pass(self):  
        r = self.app.get('/logout')
        self.assertEqual(r.status_code,302)

    def test_edit_profile_pass1(self): #แก้ไขโปรไฟล์
        user = global username_random
        sent = {"username": username_random, "password": self.config_test["register_pass1"]["password"]}
        r = self.app.post('/login',
                          data=sent)
        self.assertEqual(r.json,None)

        sent = {"action":self.config_test["edit_profile1"]["action"],
        "firstname":self.config_test["edit_profile1"]["firstname"],
        "lastname":self.config_test["edit_profile1"]["lastname"],
        "gender":self.config_test["edit_profile1"]["gender"]}
        r = self.app.post('/profile',data = sent)
        self.assertEqual(r.json["data"]["description"],"ระบบได้ทำการแก้ไขข้อมูลแล้ว")
    
    def test_edit_profile_pass2(self): #เปลี่ยนรหัสผ่าน
        user = global username_random
        sent = {"username":username_random, "password": self.config_test["register_pass1"]["password"]}
        r = self.app.post('/login',
                          data=sent)
        self.assertEqual(r.json,None)

        sent = {"action":self.config_test["edit_profile2"]["action"],
        "password":self.config_test["edit_profile2"]["password"],
        "conpassword":self.config_test["edit_profile2"]["conpassword"]}
        r = self.app.post('/profile',data = sent)
        self.assertEqual(r.json["data"]["description"],str.encode("utf-8","ระบบได้ทำการแก้ไขข้อมูลแล้ว"))

if __name__ == '__main__':
    unittest.main()
