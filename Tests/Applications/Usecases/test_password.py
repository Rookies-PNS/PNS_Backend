import __init__
import unittest
import sys
from icecream import ic
from Applications.Usecases.AppUsecaseExtention import *


class test_user_services(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = "test"
        print(sys._getframe(0).f_code.co_name)

    @classmethod
    def tearDownClass(cls):
        "Hook method for deconstructing the class fixture after running all tests in the class."
        print(sys._getframe(0).f_code.co_name)

    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        print("\t", sys._getframe(0).f_code.co_name)

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t", sys._getframe(0).f_code.co_name)

    def test_hashing(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t", sys._getframe(0).f_code.co_name)
        pw = "Asdfas12!@"
        hash = convert_to_Password_with_hashing(pw)
        pw_list = []
        for i in range(10):
            pw_list.append(convert_to_Password_with_hashing(pw))
        for i in pw_list:
            self.assertEqual(hash, i)

    def test_규칙_준수한_Password(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        pw_list = (
            """
Abcd123!
StrongPass12@
SecurePwd$789
P@ssw0rdTest
Auth3ntic@te
Gu1d3lin3!
Complic@t3dPwd
Passw0rd!123
SafeP@ssw0rd
Ch@ll3ngingPwd
P@ssw0rd!123
Secur3Pwd&456
G0odPa$$word!
TrickyP@ss789
StrongP@55word
Auth3ntic@ted!
P@ssw0rd$ecure
Ch@ll3ng3Pwd!
1LoveMyP@ss!
Saf3P@ssword!
""".lstrip()
            .rstrip()
            .split("\n")
        )
        for pw in pw_list:
            self.assertTrue(check_valid_password(pw))

    def test_규칙_준수_안한_Password(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        pw_list = (
            """
simplepassword
123456789
abcdabcd
P@ssword
qwertyui
passWORD123
1qaz2wsx
1234abcd
iloveyou
Pa$$word
s1A!
Pa$ word3
""".lstrip()
            .rstrip()
            .split("\n")
        )
        for pw in pw_list:
            self.assertFalse(check_valid_password(pw))

    def test_SQL_injection_Password(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        pw_list = (
            """
'; DROP TABLE users;--
admin'--
123' OR '1'='1';--
password' OR 'x'='x';--
'; SELECT * FROM information_schema.tables;--
admin' UNION SELECT 1,2,3;--
test'; INSERT INTO users (id, pw, account, name) VALUES (100, 'hacked', 'hacked', 'hacked');--
'; UPDATE users SET pw = 'newpassword' WHERE account = 'admin';--
evil';--
'; EXEC xp_cmdshell('cmd.exe');--
""".lstrip()
            .rstrip()
            .split("\n")
        )
        for pw in pw_list:
            self.assertFalse(check_valid_password(pw))

    def test_CSRF_Password(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        pw_list = (
            """
<img src="http://example.com/change_password?new_password=hacked">
<script>document.location='http://example.com/change_password?new_password=hacked';</script>
<form action="http://example.com/change_password" method="POST"><input type="hidden" name="new_password" value="hacked"><input type="submit" value="Submit"></form>
<a href="http://example.com/change_password?new_password=hacked" style="display:none" id="malicious-link">Click me</a><script>document.getElementById('malicious-link').click();</script>
<a href="http://example.com/change_password?new_password=hacked" style="display:none" id="malicious-link">Complic@t3dPwd</a><script>document.getElementById('malicious-link').click();</script>
<iframe src="http://example.com/change_password?new_password=hacked"></iframe>
<img src="http://example.com/logout"> (로그아웃을 유도하여 다시 인증시도시 피해를 주는 예시)
<script>fetch('http://example.com/change_password', {method: 'POST', body: 'new_password=hacked', credentials: 'include'});</script>
<img src="http://example.com/delete_account"> (계정 삭제를 유도하여 피해를 주는 예시)
<form action="http://example.com/delete_account" method="POST"><input type="hidden" name="confirm" value="true"><input type="submit" value="Submit"></form>
<a href="http://example.com/delete_account" style="display:none" id="delete-link">Click me</a><script>document.getElementById('delete-link').click();</script>
""".lstrip()
            .rstrip()
            .split("\n")
        )
        for pw in pw_list:
            self.assertFalse(check_valid_password(pw))

    def test_흔한_Password(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        pw_list = (
            """
password123
qwerty
123456
admin
letmein
welcome
123abc
1234
test
abc123
""".lstrip()
            .rstrip()
            .split("\n")
        )
        for pw in pw_list:
            self.assertFalse(check_valid_password(pw))


def main():
    unittest.main()


if __name__ == "__main__":
    main()
