'''
RSA算法，它通常是先生成一对RSA密钥，其中之一是保密密钥，由用户保存；
另一个为公开密钥，可对外公开，甚至可在网络服务器中注册。为提高保密强度，
RSA密钥至少为500位长，一般推荐使用1024位。这就使加密的计算量很大。
为减少计算量，在传送信息时，常采用传统加密方法与公开密钥加密方法相结合的方式，
即信息采用改进的DES或IDEA密钥加密，然后使用RSA密钥加密对话密钥和信息摘要。
对方收到信息后，用不同的密钥解密并可核对信息摘要。

1. 随意选择两个大的质数p和q，p不等于q，计算N=pq。
2. 根据欧拉函数，不大于N且与N互质的整数個数為(p-1)(q-1)。
3. 选择一个整数e与(p-1)(q-1)互质，并且e小于(p-1)(q-1)。
4. 用以下这个公式计算d：d× e ≡ 1 (mod (p-1)(q-1))。
5. 将p和q的记录销毁。

(N,e)是公钥，(N,d)是私钥。

+加密，解密
'''
import random


# 生成大的素数,将Miller进行k次，将合数当成素数处理的错误概率最多不会超过4^(-k)
def getprime():
    Min = 10**152;Max = 10**154;p = 0
    while(1):
        p = random.randrange(Min, Max, 1)
        # 这里进行素数验证
        if MillerRabin(p, 20) == False:
                continue
        else:
                return p

def fast_power(base, power, n):
    result = 1
    tmp = base
    while power > 0:
        if power&1 == 1:
            result = (result * tmp) % n
        tmp = (tmp * tmp) % n
        power = power>>1
    return result

# MillerRabin
def MillerRabin(n, iter_num):
    # 2 is prime
    if n == 2:
        return True
    # if n is even or less than 2, then n is not a prime
    if n&1 == 0 or n<2:
        return False
    # n-1 = (2^s)m
    m,s = n - 1,0
    while m&1==0:
        m = m>>1
        s += 1
    # M-R test
    for _ in range(iter_num):
        b = fast_power(random.randint(2,n-1), m, n)
        if b==1 or b== n-1:
            continue
        for __ in range(s-1):
            b = fast_power(b, 2, n)
            if b == n-1:
                break
        else:
            return False
    return True

# 判断互质，用辗转相除法判断最大公因数是否为1
def gcd(a, b):
    while a%b != 0:
        temp = b
        b = a%b
        a = temp
    return b

# 求模反元素
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b%a, a)
        return g, x - (b//a) * y, y

# 生成公钥、密钥
def get_key():
    # 随意选择两个大的质数p和q，p不等于q，计算N=pq
    p = getprime()
    q = getprime()
    N = p*q
    # 欧拉函数
    N_num = (p-1) * (q-1)
    # 选择e与N_num互质,且e小
    while 1:
        e = random.randint(1, N_num)
        if gcd(N_num, e) == 1:
            break
    _,x,_ = egcd(e, N_num)
    d = x % N_num
    # 返回公钥私钥
    # print(hex(p))
    # print(hex(q))
    return "{:0256X}".format(e), "{:0256X}".format(d), "{:0256X}".format(N)

# 加密
def encrypt(m, n, e):
    entext = ""
    n_len = 256
    for i in range(0, len(str(m)), 8):
        if len(str(m))-i <= 8:
            m_1 = int(ascii2hex(str(m)[i:]), 16)
        else:
            m_1 = int(ascii2hex(str(m)[i:i+8]), 16)
        text = hex(MODs(m_1, n, e))[2:]
        if len(text) < n_len:
            text = '0'*(n_len-len(text)) + text
        entext += text
    return entext

# 解密
def decrypt(c, n, d):
    detext = ""
    n_len = 256
    for i in range(0, len(c), n_len):
        c_1 = int(c[i: i+n_len], 16)
        m = hex(MODs(c_1, n, d))[2:]
        detext += hex2ascii(m)
    return detext

# ascii to hex
def ascii2hex(a):
    h = ""
    for i in a:
        h += hex(ord(i))[2:]
    return h

# hex to ascii
def hex2ascii(h):
    a = ""
    for i in range(0, len(h), 2):
        a += chr(int(h[i:i+2], 16))
    return a

# 用于计算m^e = c(modn) 和 c^d = m(modn)
def MODs(m, n, e):
    res = 1
    while e:
        if e & 1:
            res = (res * m) % n
        m = (m * m) % n
        e >>= 1
    return res

if __name__ == "__main__":
    e, d, n = get_key()         # 生成公钥、密钥 长度为1024位
    print('e ==> {}\nd ==> {}\nn ==> {}'.format(e, d, n))
    n = int(n, 16)
    # 读取明文
    m = "I love a cute gril! ^U^"
    # m = input("输入明文:")
    if m == "":
        print('No PlainText')
    else:
        print("正在加密………………………………………………")
        entext = encrypt(m, n, int(e, 16))
        print("加密成功！密文:" + entext)
    # 读取密文
    c = entext
    if m == "":
        print('No PlainText')
    else:
        print("正在解密………………………………………………")
        detext = decrypt(c, n, int(d, 16))
        print("解密成功！明文:" + detext)


