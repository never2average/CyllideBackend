from Crypto.Cipher import AES
obj = AES.new('aesEncryptionKey', AES.MODE_CBC, 'This is an IV456')
message = "passwordpassword"
ciphertext = obj.encrypt(message)
print(ciphertext)