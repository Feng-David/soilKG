#!/usr/bin/env python3
# coding: utf-8
# File: question_classifier.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

import os
import ahocorasick

class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        #　特征词路径
        self.disease_path = os.path.join(cur_dir, 'dict/chemical.txt')
        self.department_path = os.path.join(cur_dir, 'dict/cityInfo.txt')
        self.check_path = os.path.join(cur_dir, 'dict/countyInfo.txt')
        self.drug_path = os.path.join(cur_dir, 'dict/industry.txt')
        self.food_path = os.path.join(cur_dir, 'dict/landUse.txt')
        self.producer_path = os.path.join(cur_dir, 'dict/massif.txt')
        self.symptom_path = os.path.join(cur_dir, 'dict/vadoseZone.txt')
        # 加载特征词
        self.disease_wds= [i.strip() for i in open(self.disease_path,encoding='utf-8') if i.strip()]
        self.department_wds= [i.strip() for i in open(self.department_path,encoding='utf-8') if i.strip()]
        self.check_wds= [i.strip() for i in open(self.check_path,encoding='utf-8') if i.strip()]
        self.drug_wds= [i.strip() for i in open(self.drug_path,encoding='utf-8') if i.strip()]
        self.food_wds= [i.strip() for i in open(self.food_path,encoding='utf-8') if i.strip()]
        self.producer_wds= [i.strip() for i in open(self.producer_path,encoding='utf-8') if i.strip()]
        self.symptom_wds= [i.strip() for i in open(self.symptom_path,encoding='utf-8') if i.strip()]
        self.region_words = set(self.department_wds + self.disease_wds + self.check_wds + self.drug_wds + self.food_wds + self.producer_wds + self.symptom_wds)

        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句疑问词
        self.symptom_qwds = ['化学品']
        self.cause_qwds = ['相关区县']
        self.acompany_qwds = ['行业类别']
        self.food_qwds = ['利用历史']
        self.drug_qwds = ['特征污染物']
        self.prevent_qwds = ['包气带土层性质']
        self.cureway_qwds = ['超标土壤污染物']
        self.cureprob_qwds = ['超标地下水污染物']
        self.easyget_qwds = ['相关地块']
        # self.check_qwds = ['检查', '检查项目', '查出', '检查', '测出', '试出']
        # self.belong_qwds = ['属于什么科', '属于', '什么科', '科室']
        # self.cure_qwds = ['治疗什么', '治啥', '治疗啥', '医治啥', '治愈啥', '主治啥', '主治什么', '有什么用', '有何用', '用处', '用途',
        #                   '有什么好处', '有什么益处', '有何益处', '用来', '用来做啥', '用来作甚', '需要', '要']

        print('model init finished ......')

        return

    '''分类主函数'''
    def classify(self, question):
        data = {}
        medical_dict = self.check_medical(question)
        if not medical_dict:
            return {}
        data['args'] = medical_dict
        #收集问句当中所涉及到的实体类型
        types = []
        for type_ in medical_dict.values():
            types += type_
        question_type = 'others'

        question_types = []

        # 症状
        if self.check_words(self.symptom_qwds, question) and ('disease' in types):
            question_type = 'disease_symptom'
            question_types.append(question_type)

        if self.check_words(self.symptom_qwds, question) and ('symptom' in types):
            question_type = 'symptom_disease'
            question_types.append(question_type)

        # 原因
        if self.check_words(self.cause_qwds, question) and ('disease' in types):
            question_type = 'disease_cause'
            question_types.append(question_type)
        # 并发症
        if self.check_words(self.acompany_qwds, question) and ('disease' in types):
            question_type = 'disease_acompany'
            question_types.append(question_type)

        # # 推荐食品
        # if self.check_words(self.food_qwds, question) and 'disease' in types:
        #     deny_status = self.check_words(self.deny_words, question)
        #     if deny_status:
        #         question_type = 'disease_not_food'
        #     else:
        #         question_type = 'disease_do_food'
        #     question_types.append(question_type)

        # #已知食物找疾病
        # if self.check_words(self.food_qwds+self.cure_qwds, question) and 'food' in types:
        #     deny_status = self.check_words(self.deny_words, question)
        #     if deny_status:
        #         question_type = 'food_not_disease'
        #     else:
        #         question_type = 'food_do_disease'
        #     question_types.append(question_type)

        # 推荐药品
        if self.check_words(self.drug_qwds, question) and 'disease' in types:
            question_type = 'disease_drug'
            question_types.append(question_type)

        # 药品治啥病
        if self.check_words(self.cause_qwds, question) and 'department' in types:
            question_type = 'drug_disease'
            question_types.append(question_type)

        # 疾病接受检查项目
        if self.check_words(self.acompany_qwds, question) and 'drug' in types:
            question_type = 'disease_check'
            question_types.append(question_type)

        # # 已知检查项目查相应疾病
        if self.check_words(self.easyget_qwds, question) and 'check' in types:
            question_type = 'check_disease'
            question_types.append(question_type)

        #　症状防御
        if self.check_words(self.prevent_qwds, question) and 'disease' in types:
            question_type = 'disease_prevent'
            question_types.append(question_type)

        if self.check_words(self.food_qwds, question) and 'producer' in types:
            question_type = 'food_qwds'
            question_types.append(question_type)

        if self.check_words(self.drug_qwds, question) and 'producer' in types:
            question_type = 'drug_qwds'
            question_types.append(question_type)
        if self.check_words(self.prevent_qwds, question) and 'producer' in types:
            question_type = 'prevent_qwds'
            question_types.append(question_type)
        if self.check_words(self.cureway_qwds, question) and 'producer' in types:
            question_type = 'cureway_qwds'
            question_types.append(question_type)
        if self.check_words(self.cureprob_qwds, question) and 'producer' in types:
            question_type = 'cureprob_qwds'
            question_types.append(question_type)


        # # 疾病医疗周期
        # if self.check_words(self.lasttime_qwds, question) and 'disease' in types:
        #     question_type = 'disease_lasttime'
        #     question_types.append(question_type)

        # 疾病治疗方式
        if self.check_words(self.cureway_qwds, question) and 'disease' in types:
            question_type = 'disease_cureway'
            question_types.append(question_type)

        # 疾病治愈可能性
        if self.check_words(self.cureprob_qwds, question) and 'disease' in types:
            question_type = 'disease_cureprob'
            question_types.append(question_type)

        # # 疾病易感染人群
        # if self.check_words(self.easyget_qwds, question) and 'disease' in types :
        #     question_type = 'disease_easyget'
        #     question_types.append(question_type)

        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == [] and 'disease' in types:
            question_types = ['disease_desc']

        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == [] and 'symptom' in types:
            question_types = ['symptom_disease']

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data

    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.disease_wds:
                wd_dict[wd].append('disease')
            if wd in self.department_wds:
                wd_dict[wd].append('department')
            if wd in self.check_wds:
                wd_dict[wd].append('check')
            if wd in self.drug_wds:
                wd_dict[wd].append('drug')
            if wd in self.food_wds:
                wd_dict[wd].append('food')
            if wd in self.symptom_wds:
                wd_dict[wd].append('symptom')
            if wd in self.producer_wds:
                wd_dict[wd].append('producer')
        return wd_dict

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''
    def check_medical(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)