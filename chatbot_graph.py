#!/usr/bin/env python3
# coding: utf-8
# File: chatbot_graph.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

from question_classifier import *
from question_parser import *
from answer_search import *

'''问答类'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()
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

    def chat_main(self, sent):
        data = {}
        data['rlt'] = '目前只支持部分地区土壤污染相关, 希望可以帮到您。'
        data['img'] = ''
        data['json'] = ''
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return data
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return data
        else:
            data['rlt'] = final_answers['rlt']
            data['json'] = final_answers['json']
            data['img'] = self.get_img(sent)
            return data

    def get_img(self, question):
        if self.check_words(self.symptom_qwds, question):
            return "../static/img/hxp.jpeg"
        if self.check_words(self.cause_qwds, question):
            return "../static/img/xgxq.jpg"
        if self.check_words(self.acompany_qwds, question):
            return "../static/img/hylb.jpeg"
        if self.check_words(self.food_qwds, question):
            return "../static/img/lyls.jpeg"
        if self.check_words(self.drug_qwds, question):
            return "../static/img/tzwr.jpeg"
        if self.check_words(self.prevent_qwds, question):
            return "../static/img/bqdt.jpeg"
        if self.check_words(self.cureway_qwds, question):
            return "../static/img/cbtr.jpeg"
        if self.check_words(self.cureprob_qwds, question):
            return "../static/img/dxs.jpeg"
        if self.check_words(self.easyget_qwds, question):
            return "../static/img/xgdk.jpeg"
        return ''

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False



if __name__ == '__main__':
    handler = ChatBotGraph()
    while 1:
        question = input('用户:')
        answer = handler.chat_main(question)
        print('助理:', answer)

