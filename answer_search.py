#!/usr/bin/env python3
# coding: utf-8
# File: answer_search.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-5
from flask import jsonify
from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        self.g = Graph(
            host="127.0.0.1",
            http_port=7474,
            user="neo4j",
            password="1234")
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls):
        # final_answers = {}
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                return final_answer
        return None

    def get_json_data(self, data):
        json_data = {'data': [], "links": []}
        # d = []

        # for i in data:
        #     # print(i["p.Name"], i["r.relation"], i["n.Name"], i["p.cate"], i["n.cate"])
        #     d.append(i['p.Name'] + "_" + i['p.cate'])
        #     d.append(i['n.Name'] + "_" + i['n.cate'])
        #     d = list(set(d))
        name_dict = {}
        count = 0
        for j in data:
            # j_array = j.split("_")

            data_item = {}
            # name_dict[j_array[0]] = count
            count += 1
            data_item['name'] = j['m.name']
            data_item['category'] = ''
            json_data['data'].append(data_item)
        for i in data:
            link_item = {}

            link_item['source'] = j['m.name']

            link_item['target'] = j['m.name']
            link_item['value'] = '' ##i['r.relation']
            json_data['links'].append(link_item)

        return json_data

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        data = {}
        global desc
        global json
        final_answer = []
        if not answers:
            return ''
        if question_type == 'disease_symptom':
            for key, value in answers[0]['n'].items():
                final_answer.append(key + ":" + value)
            desc = ','.join(final_answer)
            #subject = answers[0]['m.name']
            #final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'symptom_disease':
            desc = [i['m.name'] for i in answers]
            json = self.get_json_data(answers)
            #subject = answers[0]['n.name']
            #final_answer = '症状{0}可能染上的疾病有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cause':
            desc = [i['m.cause'] for i in answers]
            #subject = answers[0]['m.name']
            #final_answer = '{0}可能的成因有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_prevent':
            desc = [i['m.prevent'] for i in answers]
            #subject = answers[0]['m.name']
            #final_answer = '{0}的预防措施包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_lasttime':
            desc = [i['m.cure_lasttime'] for i in answers]
            #subject = answers[0]['m.name']
            #final_answer = '{0}治疗可能持续的周期为：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cureway':
            desc = [';'.join(i['m.cure_way']) for i in answers]
            #subject = answers[0]['m.name']
            #final_answer = '{0}可以尝试如下治疗：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cureprob':
            desc = [i['m.cured_prob'] for i in answers]
            #subject = answers[0]['m.name']
            #final_answer = '{0}治愈的概率为（仅供参考）：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_easyget':
            desc = [i['m.easy_get'] for i in answers]
            #subject = answers[0]['m.name']

            #final_answer = '{0}的易感人群包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_desc':
            desc = [i['m.desc'] for i in answers]
            #subject = answers[0]['m.name']
            #final_answer = '{0},熟悉一下：{1}'.format(subject,  '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_acompany':
            desc1 = [i['n.name'] for i in answers]
            desc2 = [i['m.name'] for i in answers]
            #subject = answers[0]['m.name']
            desc = [i for i in desc1 + desc2 if i != subject]
            #final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_not_food':
            desc = [i['n.name'] for i in answers]
            #subject = answers[0]['m.name']
            #final_answer = '{0}忌食的食物包括有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_do_food':
            desc = [i['n.name'] for i in answers]
            #recommand_desc = [i['n.name'] for i in answers if i['r.name'] == '推荐食谱']
            #subject = answers[0]['m.name']
            #final_answer = '{0}宜食的食物包括有：{1}\n推荐食谱包括有：{2}'.format(subject, ';'.join(list(set(do_desc))[:self.num_limit]), ';'.join(list(set(recommand_desc))[:self.num_limit]))

        elif question_type == 'food_not_disease':
            desc = [i['m.name'] for i in answers]
            json = self.get_json_data(answers)
            #subject = answers[0]['n.name']
            #final_answer = '患有{0}的人最好不要吃{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)

        elif question_type == 'food_do_disease':
            desc = [i['m.name'] for i in answers]
            json = self.get_json_data(answers)
            #subject = answers[0]['n.name']
            #final_answer = '患有{0}的人建议多试试{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)

        elif question_type == 'disease_drug':
            desc = [i['n.name'] for i in answers]
            #subject = answers[0]['m.name']
            #final_answer = '{0}通常的使用的药品包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'drug_disease':
            d = [i['m.name'] for i in answers]
            json = self.get_json_data(answers)
            desc = ','.join(d)
            #subject = answers[0]['n.name']
            #final_answer = '{0}主治的疾病有{1},可以试试'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_check':
            d = [i['m.name'] for i in answers]
            json = self.get_json_data(answers)
            desc = ','.join(d)
            #subject = answers[0]['m.name']
            #final_answer = '{0}通常可以通过以下方式检查出来：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        #food_qwds
        elif question_type == 'food_qwds':
            d = [i['m.name'] for i in answers]
            json = self.get_json_data(answers)
            desc = ','.join(d)
        elif question_type == 'drug_qwds':
            d = [i['m.name'] for i in answers]
            json = self.get_json_data(answers)
            desc = ','.join(d)
        elif question_type == 'check_disease':
            d = [i['m.name'] for i in answers]
            json = self.get_json_data(answers)
            desc = ','.join(d)
        elif question_type == 'prevent_qwds':
            d = [i['m.name'] for i in answers]
            json = self.get_json_data(answers)
            desc = ','.join(d)
        elif question_type == 'cureway_qwds':
            d = [i['m.name'] for i in answers]
            json = self.get_json_data(answers)
            desc = ','.join(d)
        elif question_type == 'cureprob_qwds':
            d = [i['m.name'] for i in answers]
            json = self.get_json_data(answers)
            desc = ','.join(d)
            # subject = answers[0]['n.name']
            #final_answer = '通常可以通过{0}检查出来的疾病有{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        data['rlt'] = desc
        data['json'] = json
        return data


if __name__ == '__main__':
    searcher = AnswerSearcher()
