import unittest
import sys
from radicaltest import dealRadical
from mixtest import dealelse
##测试主要分析函数dealradical与dealelse
##没有问题的测试点不加说明
class radicalTest1(unittest.TestCase):

    def test_radicaltest(self):
        wordlist1 = ["你好", "好穷"]
        wordradical1 = ["亻女", "女穴"]
        linetest1 = "吃饭睡  觉上床   亻尔女子一 起吃饭谢 谢你 是个好人我真的  女子穴力啊 "
        ans_excepted="<你好>亻尔女子\n<好穷>女子穴力\n"
        ans_my=dealRadical(wordradical1,linetest1,wordlist1)
        self.assertEqual(ans_excepted,ans_my)




    def test_radicaltest2(self):
        wordlist2 = ["上下左右", "你是法轮功"]
        wordradical2 = ["一一工口", "亻日氵车力"]
        linetest2 = "吃饭睡  ⺊一一⺊力工力口觉上床   一 起吃亻尔日疋氵去车仑工力饭谢 谢你 是个好人我真的  女子穴力啊 "
        ans_excepted="<上下左右>⺊一一⺊力工力口\n<你是法轮功>亻尔日疋氵去车仑工力\n"
        ans_my=dealRadical(wordradical2,linetest2,wordlist2)
        self.assertEqual(ans_excepted,ans_my)
##第一个问题：对于一个汉字拆分后的两个汉字，如果其中的汉字仍可以继续拆分，则输出内容会错误
#

    def test_radicaltest3(self):
        wordlist3 = ["谢谢"]
        wordradical3= ["讠讠"]
        linetest3= "吃饭睡  ⺊一一⺊力工力口觉上床讠射讠射   一 起吃亻尔日疋氵去车仑工力饭谢 谢你 是个好人我真的  女子穴力啊 "
        ans_excepted="<谢谢>讠射讠射\n"
        ans_my=dealRadical(wordradical3,linetest3,wordlist3)
        self.assertEqual(ans_excepted,ans_my)


    def test_radicaltest4(self):
        wordlist4 = ["起床"]
        wordradical4 = ["走广"]
        linetest4 = "吃饭睡  ⺊一一⺊力工力口觉上床走己广木讠射讠射   起吃一一亻尔日疋氵去车仑工力饭谢 谢你 是个好人我真的  女子穴力啊 "
        ans_excepted="<起床>走己广木\n"
        ans_my=dealRadical(wordradical4,linetest4,wordlist4)
        self.assertEqual(ans_excepted,ans_my)
##第二个问题：如果汉字不可拆分，比如一的部首仍是一，则也会输出错误

    def test_radicaltest5(self):
        wordlist5= ["一二三"]
        wordradical5 = ["一二一"]
        linetest5 = "吃饭睡  ⺊一二一二⺊力工力口觉上床走己广木讠射讠射   起吃一二一二亻尔日疋氵去车仑工力饭谢 谢你 是个好人我真的  女子穴力啊 "
        ans_excepted="<一二三>一二一二\n"
        ans_my=dealRadical(wordradical5,linetest5,wordlist5)
        self.assertEqual(ans_excepted,ans_my)

    def test_mixtest1(self):
        wordlistori=["起床",'吃饭','上下左右']
        wordlist=["qichuang",'qi床','q床','chif','上xia左you',"s下左右"]
        line='qichuang饭睡  ⺊一qi床一⺊q床力工力口chif觉上s下左右xia左you上床走己广木讠射讠射 '
        line2=line
        ans_excepted = "<起床>qichuang\n<起床>qi床\n<起床>q床\n<吃饭>chif\n<上下左右>s下左右\n<上下左右>上xia左you\n"
        ans_my = dealelse(line,wordlist,line2,wordlistori)
        self.assertEqual(ans_excepted, ans_my)

    def test_mixtest1(self):
        wordlistori = ["起床", '吃饭', '上下左右']
        wordlist = ["qc", 'qchuang', 'sxzy', "s下z右"]
        line = '饭睡  qc⺊一一⺊力工力qchuang口sxzy上s下左右床走己s下z右广木讠射讠射 '
        line2 = line
        ans_excepted = "<起床>qc\n<起床>qchuang\n<上下左右>sxzy\n<上下左右>s下z右\n"
        ans_my = dealelse(line, wordlist, line2, wordlistori)
        self.assertEqual(ans_excepted, ans_my)


    def test_mixtest1(self):
        wordlistori = ["离开", '家乡', '去种田']
        wordlist = ["likai",'lkai','l开', 'jiaxiang', "qzt","去种t"]
        line = '饭睡  qc⺊likai一一⺊力lkai工力qchl开uang口sxzyjiaxiang上s下左右qzt床走己s下z右去种t广木讠射讠射 '
        line2 = line
        ans_excepted = "<离开>likai\n<离开>lkai\n<离开>l开\n<家乡>jiaxiang\n<去种田>qzt\n<去种田>去种t\n"
        ans_my = dealelse(line, wordlist, line2, wordlistori)
        self.assertEqual(ans_excepted, ans_my)


    def test_mixtest4(self):
        wordlistori = ["难受", 'hhh', 'fuckme']
        wordlist = ["nanshou", 'hhh',"fuckme"]
        line = '饭睡  qc⺊likai一nanshou一⺊力lkh h  hai工力qchl开uang口sxfu  c k  mezyjiaxiang上s下左右qzt床走己s下z右去种t广木讠射讠射 '
        line2 = line
        ans_excepted = "<难受>nanshou\n<hhh>h h  h\n<fuckme>fu  c k  me\n"
        ans_my = dealelse(line, wordlist, line2, wordlistori)
        self.assertEqual(ans_excepted, ans_my)

    def test_mixtest5(self):
        wordlistori = ['吃大餐',"难受", 'hhh', 'fuckme']
        wordlist = ["吃大餐","难受", 'hhh',"fuckme"]
        line = '饭睡  qc⺊lik迟搭残ai一n男瘦shou一⺊力lkh h  h hhh ai工力qchl开uang口sxfu  c k  mezyjiaxiang上s下左右qzt床走己s下z右去种t广木讠射讠射 '
        line2 = line
        ans_excepted = "<吃大餐>迟搭残\n<难受>男瘦\n<hhh>h h  h\n<fuckme>fu  c k  me\n<hhh>hhh\n"
        ans_my = dealelse(line, wordlist, line2, wordlistori)
        self.assertEqual(ans_excepted, ans_my)

    def test_input(self):
        try:
            fileorg = open(sys.argv[2], encoding='utf8')
            filewords = open(sys.argv[1], encoding='utf8')
            ans = open(sys.argv[3], mode='w')
        except :
            print("输入参数错误")


if __name__ == '__main__':
    unittest.main()
