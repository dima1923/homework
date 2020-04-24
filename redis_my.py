import os
from redis.sentinel import Sentinel
from time import sleep

containers_name = {
    "master": "redis_master",
    "sentinel1": "redis_sentinel1",
    "slave1": "redis_slave1",
    "sentinel2": "redis_sentinel2",
    "slave2": "redis_slave2",
    "sentinel3": "redis_sentinel3"
}

os.system('docker-compose up -d')
sleep(15)
sentinel = Sentinel([('localhost', 6666),('localhost', 7777),('localhost', 8888)], socket_timeout=0.1)
print(sentinel.discover_master('mymaster'))
master = sentinel.master_for('mymaster')
my_dict = {'key'+str(i):'value'+str(i) for i in range(0,20)}
for k,v in my_dict.items():
    master.set(k,v)
print("покажем результат добавления")
for k in my_dict.keys():
    print(master.get(k))
sleep(3)
print("выключаем мастера")
os.system('docker stop %s'%containers_name["master"])
print("выключаем первый сентинел")
os.system('docker stop %s'%containers_name["sentinel1"])
sleep(60)
master1 = sentinel.master_for('mymaster')
print('новый мастер:'+sentinel.discover_master('mymaster').__str__())
print("данные с нового мастера")
for key in my_dict.keys():
    print(master1.get(key))
print('останавливаем и удаляем контейнеры')
for container in containers_name.values():
    os.system("docker stop %s" % container)
    os.system("docker rm %s" % container)