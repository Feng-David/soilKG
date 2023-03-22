from django.shortcuts import render
import sys

# Create your views here.
from KGQA_Based_On_medicine.settings import HANDLER
from chatbot_graph import ChatBotGraph


def search_post(request):
    ctx = {}
    question = ''
    if request.POST:
        question = request.POST['q']
    if request.GET:
        question = request.GET['q']

    ctx = HANDLER.chat_main(question)
    print(ctx['rlt'])
    print(ctx['img'])
    ctx['req'] = question
    return render(request, "post.html", ctx)


# def query(name):
#     data = graph.run(
#         "match(p )-[r]->(n:Person{Name:'%s'}) return  p.Name,r.relation,n.Name,p.cate,n.cate\
#             Union all\
#         match(p:Person {Name:'%s'}) -[r]->(n) return p.Name, r.relation, n.Name, p.cate, n.cate" % (name, name)
#     )
#     data = list(data)
#     return get_json_data(data)

