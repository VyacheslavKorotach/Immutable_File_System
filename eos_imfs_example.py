from eos_imfs import EosFile
from eos_imfs import EosDir

#file_1 = EosFile('destitutecat', '/Users/slava/PycharmProjects/Immutable_File_System', 'test_file_02.txt', 'wealthysnake', 'privat_key')
#file_1 = EosFile('destitutecat', '/Users/slava/PycharmProjects/Immutable_File_System', 'Anatoliy.jpg', 'wealthysnake', 'privat_key')
file_1 = EosFile('destitutecat', '/Users/slava/PycharmProjects/Immutable_File_System/test', 'Anatoliy.jpg', 'wealthysnake', 'privat_key')
file_1.ping()  # test of class
# s0 = file_1.__encode_file('string2')
# file_1.__decode_file(s0)
print(file_1.account)
print(file_1.path)
print(file_1.file_name)
#file_1.put_file()
#file_1.update_dir(12345678)
#print(file_1.get_dir())
#file_1.get_file()
#file_1.test_send()
#file_1.get_transaction_test()
#file_1.get_block()
#file_1.get_last()

# download dir
dir_1 = EosDir('destitutecat', '/Users/slava/PycharmProjects/Immutable_File_System/test', 'wealthysnake', 'privat_key')
dir_1.get_dir()

# upload file
file_1 = EosFile('destitutecat', '/Users/slava/PycharmProjects/Immutable_File_System/test', 'Anatoliy.jpg', 'wealthysnake', 'privat_key')
file_1.put_file()