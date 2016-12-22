# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser

class CityParser(HTMLParser):
    '''川崎市バスのバスなびHTML解析パーサ
    PC用のHTMLから必要な情報をぬきとる
    '''

    def __init__(self):
        '''初期化'''
        HTMLParser.__init__(self)
        self.table_depth = 0
        self.tr_count = 0
        self.td_index = 0
        self.buslist = list()
        self.td_flag = False
        self.Target_depth = 3

    def setTableStart(self):
        '''継承できるようにテーブルのカウントを切り出しておいた'''
        self.table_depth = self.table_depth+1

    def setTableEnd(self):
        '''継承できるようにテーブルのカウントを切り出しておいた
        市バスは入れ子になっているので、閉じタグで階層を戻してあげる必要がある
        '''
        self.table_depth = self.table_depth-1

    def handle_starttag(self, tag, attrs):
        '''開始タグ判定
        table,tr,tdの判定に使用する
        '''
        if tag == "table":
            self.setTableStart()
        elif self.table_depth == self.Target_depth:
            if tag == "tr":
                self.tr_count = self.tr_count + 1
                self.current = list()
            if tag == "td" or tag == "th":
                self.td_flag = True

    def handle_endtag(self, tag):
        '''終了タグ判定
        table,tr,tdの判定に使用する
        '''
        if tag == "table":
            self.setTableEnd()
        elif self.table_depth == self.Target_depth:
            if tag == "tr" :
                self.buslist.append(self.current)
            if tag == "td" or tag=="th":
                self.td_flag = False

    def handle_data(self, data):
        '''データ取得
        各種フラグを見て格納先を選択
        '''
        if self.td_flag:
            self.current.append(data)
            
    def getlist(self):
        '''ディクショナリのリストを生成
        HTMLから拾ってきたデータにラベル付したディクショナリに変換
        '''

        result=list()
        for row in self.buslist[1:]:
            dict={
                'prediction':row[1],
                'timetable':row[0],
                'gate':	row[2].replace(u'番のりば',''),
                'route':row[3],
                'destination':row[4],
                'vihicle':row[6],
                'situation':row[7].replace(u'します',''),
                'arrival':row[8],
                'operator':u"川崎",
            }
            result.append(dict)
        return result

class RinkoParser(CityParser):
    '''臨港バスのバスなびHTML解析パーサ
    市バスのパーサから継承。
    '''
    
    def __init__(self):
        '''初期化'''
        CityParser.__init__(self)
        self.Target_depth=4

    def setTableEnd(self):
        '''テーブルの終了タグ処理
        臨港バスはテーブルが並列に並んでいるので閉じタグは気にしない
        '''
        pass

    def getlist(self):
        '''ディクショナリのリストを生成
        市バスと並び順が違うので独自実装が必要なのさ
        '''
        result=list()
        for row in self.buslist[1:]:
            dict={
                'prediction':row[1],
                'timetable':row[0],
                'gate':	row[4],
                'route':row[5],
                'destination':row[6],
                'vihicle':row[9],
                'situation':row[2].replace(u'します',''),
                'arrival':row[3],
                'operator':u"臨港",
            }
            result.append(dict)
        return result
