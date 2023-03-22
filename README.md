启动项目： python3 manage.py runserver


【实体和关系说明】

【实体构建】：
        【实体】城市 cityInfo 
        【实体】区县 countyInfo
        【实体】地块  massif
        【实体】行业类别 industry
        【实体】地块利用历史  landUse
        【实体】化学品 chemical
        【实体】包气带土层 vadoseZone

【创建关系】：
        【关系】 【cityTocounty】省市
        【关系】【massifTocounty】地块-区县
        【关系】【massifToindustry】地块-行业类别
        【关系】【massifToclass】地块-行业门类
        【关系】【massifTolandUse】地块-地块利用
        【关系】【classToclass】行业门类-行业门类  
        【关系】【massifTochemical】地块-化学品 （关系名：特征污染物、超标土壤污染物、超标地下水污染物、土壤污染区超标土壤污染物、地下水污染区超标地下水污染物）
        【关系】【massifTovadoseZone】地块-包气带土层

1、检索实体数据：
# 查询荔湾区的相关地块
MATCH p=(n:countyInfo{name:'荔湾区'})<-[r:massifTocounty]-(m:massif) RETURN p

# 查询化学品为"氨基甲烷"的
MATCH p=(n:chemical{name:'氨基甲烷'}) RETURN p

# 查询"广州市"相关区县
MATCH p=(n:cityInfo{name:'广州市'})-[r:cityTocounty]->(m) RETURN p

# 查询广州市荔湾区精彩印花厂地块的行业类别
MATCH p=(n:massif{name:'广州市荔湾区精彩印花厂地块'})-[r:massifToindustry]->(m:industry) RETURN p

# 查询广州安华电子有限责任公司地块的利用历史
MATCH p=(n:massif{name:'广州安华电子有限责任公司地块'})-[r:massifTolandUse]->(m:landUse) RETURN p

# 查询广州安华电子有限责任公司地块的特征污染物
MATCH p=(n:massif{name:'广州安华电子有限责任公司地块'})-[r:massifTochemical]->(m:chemical) 
WHERE r.name = '特征污染物'
RETURN p

# 查询广州市悦诚安纤维制品有限公司地块的包气带土层性质
MATCH p=(n:massif{name:'广州市悦诚安纤维制品有限公司地块'})-[r:massifTovadoseZone]->(m:vadoseZone) RETURN p

# 查询广州新市黄边电镀厂地块的超标土壤污染物
MATCH p=(n:massif{name:'广州新市黄边电镀厂地块'})-[r:massifTochemical]->(m:chemical) 
WHERE r.name = '超标土壤污染物'
RETURN p   

# 查询河源市鸿伟矿业有限公司连平县油溪焦园桂林铁矿分公司地块的超标地下水污染物
MATCH p=(n:massif{name:'河源市鸿伟矿业有限公司连平县油溪焦园桂林铁矿分公司地块'})-[r:massifTochemical]->(m:chemical) 
WHERE r.name = '超标地下水污染物'
RETURN p  