from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import os

# 加密密钥，长度应为16的倍数
key = b'this_is_a_key123'

# 加密函数
def encrypt_image(image_path, output_path):
    with open(image_path, 'rb') as image_file:
        raw_data = image_file.read()

    # 创建AES对象并进行加密
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted_data = cipher.encrypt(pad(raw_data, AES.block_size))

    # 生成随机的IV（初始化向量）并附加到加密数据后面
    iv = cipher.iv
    encrypted_data = iv + encrypted_data

    # 将加密数据写入输出文件
    with open(output_path, 'wb') as output_file:
        output_file.write(encrypted_data)

    print("Image encrypted successfully!")

# 解密函数
def decrypt_image():
    # 打开加密图片并读取数据
    encrypted_path = 'ITF_Team_Photo_encrypted.jpg'
    output_path = 'ITF_Team_Photo_decrypted.jpg'
    with open(encrypted_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()

    # 提取IV（初始化向量）和加密数据
    iv = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]

    key = b'this_is_a_key123'
    # 创建AES对象并进行解密
    cipher = AES.new(key, AES.MODE_CBC, iv)
    raw_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    # 将解密后的数据写入输出文件
    with open(output_path, 'wb') as output_file:
        output_file.write(raw_data)

    print("Image decrypted successfully!")



encrypt_image('ITF_Team_Photo.jpg', 'ITF_Team_Photo_encrypted.jpg')

decrypt_image()

# # 使用示例：加密和解密图片
# input_image = 'ITF_Team_Photo.jpg'  # 输入图片路径
# encrypted_image = 'ITF_Team_Photo_encrypted.jpg'  # 加密后图片路径
# decrypted_image = 'ITF_Team_Photo_decrypted.jpg'  # 解密后图片路径
#
# # 加密图片
# encrypt_image(input_image, encrypted_image)

# 解密图片
# decrypt_image(encrypted_image, decrypted_image)

