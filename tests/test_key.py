import pytest
import securechat.key as k

class Test_decrypt:
    def test_decrypt(self):
        private, public = k.loadKeys()
        txt = "anirut"
        
        cipher = k.encrypt(txt,public)
        decrypted = k.decrypt(cipher,private)

        assert txt == decrypted


        