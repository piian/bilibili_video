from bilibili_api import Bilibili

cid = '19516333'
# 短
cid = '32170391'
# 系列
cid = '32317625'
# 3小时教你入门numpy
cid = '50452482'
cid = '32170391'
cid = '19817183'
cid = '98652168'
cid = '94404010'  # 大型网站Mysql性能优化之索引原理分析 (完成)
cid = '97555923'  # 2020PHP高级面试跳槽必备技术—高可用MySQL优化方案之分库分表 （完成）
cid = '90856027'  # PHP高并发解决方案-服务通讯rpc接口开发 （完成）

cid = '752922075'  # 单人
cid = '242936413'  # 测试

client = Bilibili()

client.get_list(cid)
