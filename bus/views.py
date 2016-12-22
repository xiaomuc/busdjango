# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse
from django.views import generic
import django.utils.encoding  
import urllib2
import busparser

from .models import Line

class IndexView(generic.ListView):
    '''インデックスページ
    バスの乗り場+行き先パターンをデータベースから拾ってきてリスト表示する
    '''
    template_name = 'bus/index.html'
    context_object_name='line_list'
    def get_queryset(self):
        """バスの乗り場+行き先パターンをデータベースから拾ってきてリスト表示する"""
        return Line.objects.all()

def detail(request, line_id):
    '''個別の時刻表示ページ
    DBから市バス、臨港バス用のパラメータ値を持ってきて各ページから情報を取る
    取得したHTMLを解析して一覧を作成、ソートして表示する
    '''
    # DBから情報取ってくる
    line = get_object_or_404(Line, pk=line_id)

    # 各社サイトのURL編集
    url_city=r"http://www.kcbn.jp/loca/depArr/DepArrDspStatus.asp?ID=2011051019230470&DepKey={dep}&ArrKey={arr}".format(dep=line.city_dep,arr=line.city_arr)
    url_rinko=r"http://www.rinkobus-navi.jp/blsys/loca?VID=lsc&EID=nt&DSMK={dep}&ASMK={arr}".format(dep=line.rinko_dep,arr=line.rinko_arr)

    # 各社サイトから情報取得
    result_city=urllib2.urlopen(url_city)
    result_rinko=urllib2.urlopen(url_rinko)
    
    # 取得したHTMLの解析
    parser_city=busparser.CityParser()
    parser_rinko=busparser.RinkoParser()
    parser_city.feed(unicode(result_city.read(),'cp932'))
    parser_rinko.feed(unicode(result_rinko.read(),'cp932'))
    
    # マージとソート
    mergelist = parser_city.getlist() + parser_rinko.getlist()
    sortedlist=sorted(mergelist,key=lambda x:x['prediction'])

    return render(request,'bus/detail.html',{
        'buslist':sortedlist,
        'url_city':url_city,
        'url_rinko':url_rinko,
        'text_dep':line.text_dep,
        'text_arr':line.text_arr,
    })
