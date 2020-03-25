import struct
import time
import snap7


def plc_con_close(client):
    '''
    连接关闭
    :param client:
    :return:
    '''
    client.disconnect()

def test_mk10_1(client):
    '''
    测试M10.1
    :return:
    '''
    area = snap7.snap7types.areas.MK
    dbnumber = 0
    amount = 1
    start = 10
    print(u'初始值')
    mk_data = client.read_area(area, dbnumber, start, amount)
    print(struct.unpack('!c', mk_data))

    print(u'置1')
    client.write_area(area, dbnumber, start, b'\x01')
    print(u'当前值')
    mk_cur = client.read_area(area, dbnumber, start, amount)
    print(struct.unpack('!c', mk_cur))

def test_mk_w201(client):
    '''
    测试MW201,数据类型为word
    :param client:
    :return:
    '''
    area = snap7.snap7types.areas.MK
    dbnumber = 0
    amount = 2
    start = 201
    print(u'初始值')
    mk_data = client.read_area(area, dbnumber, start, amount)
    print(struct.unpack('!h', mk_data))

    print(u'置12')
    client.write_area(area, dbnumber, start, b'\x00\x0C')
    print(u'当前值')
    mk_cur = client.read_area(area, dbnumber, start, amount)
    print(struct.unpack('!h', mk_cur))

    time.sleep(3)
    print(u'置3')
    client.write_area(area, dbnumber, start, b'\x00\x03')
    print(u'当前值')
    mk_cur = client.read_area(area, dbnumber, start, amount)
    print(struct.unpack('!h', mk_cur))



def plc_connect(ip, type, rack=0, slot=1):
    """
    连接初始化
    :param ip:
    :param type::param connection_type: 1 for PG, 2 for OP, 3 to 10 for S7 Basic
    :param rack: 通常为0   
    :param slot: 根据plc安装，一般为0或1
    :return:client
    """
    client = snap7.client.Client()
    client.set_connection_type(type)
    client.connect(ip, rack, slot)
    return client

def plc_con_close(client):
    """
    连接关闭
    :param client:
    :return:
    """
    client.disconnect()

#### V区就是DB区的B区
def read_VB(client, offset):
    """ :param client: client
        :param offset: int 
        :returns: str.
    """
    vb_data = client.db_read(1, offset, 1)
    return vb_data[0]

def write_VB(client, offset, data):
    """ :param client: client
        :param offset: int 
        :param data: str
    """
    data = int(data)
    temp = hex(int(data))[2:]
    if data < 0 or data > 255:
        print("请输入0-255之间的数")
    else:
        if data < 16:
            temp = "0"+ temp
        client.db_write(1, offset, bytes.fromhex(temp))
        print("向寄存器VB"+str(offset)+"写入"+str(data)+"成功")

if __name__ == "__main__":

    client_fd = plc_connect('192.168.2.1', 2)
    print("connect success")    
    write_VB(client_fd, 1, "16")
    
    
    
    data = read_VB(client_fd, 1)
    print(data)
    
    
    
    test_mk10_1(client_fd)
    test_mk10_1(client_fd)
    
    
    plc_con_close(client_fd)
    
    

