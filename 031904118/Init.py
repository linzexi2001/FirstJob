import re
from xpinyin import Pinyin
from cnradical import Radical, RunOption
p=Pinyin()
radical = Radical(RunOption.Radical)

#判断是否为汉字
def ischinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True

##得到敏感词的每个汉字的偏旁，并以字符串的形式返回
def find(string):
        str=[]
        radical = Radical(RunOption.Radical)
        str1 = [radical.trans_ch(ele) for ele in string]
        s=''.join(str1)
        return s

##预处理敏感词表 返回包含各种形式的替换敏感词表wordList，初始敏感词表,Word_Basic，偏旁部首表apart
def preword(filewords):
    Word_Basic = []
    apart = []
    wordList = []
    ##遍历每个敏感词
    for words in filewords:
        words=words.strip("\n")
        ##先将原始敏感词加入wordList
        wordList.append(words)
        ##得到原始敏感词表Word_Basic
        Word_Basic.append(words)
        allpinyin = p.get_pinyin(words, '')
        ##将敏感词的全拼音形式加入wordList
        wordList.append(allpinyin)
        firstpinyin=p.get_initials(words,'')
        wordList.append(firstpinyin.lower())
        ##将敏感词的偏旁部首列表加入列表apart
        if ischinese(words):
            apratword=find(words)
            apart.append(apratword)

        ##遍历一个敏感词将形如法l功，X教的首字符替换形式加入wordList
        for everyword in words:
             m = re.sub(everyword, p.get_pinyin(everyword, ''), words)
             pinyin_low = re.sub(everyword, p.get_initial(everyword, '').lower(), words)
             wordList.append(m)
             wordList.append(pinyin_low)

        ##遍历一个敏感词，将形如FaLG,FLunG的混合字符替换形式加入wordList
        for aWord in range(words.__len__()):
            m=p.get_initials(words,'')
            t=re.sub(m[aWord], p.get_pinyin(words[aWord], ''), m)
            wordList.append(t)

    ##wordList去重
    orgList =wordList
    wordList= []
    for id in orgList:
        if id not in wordList:
            wordList.append(id)
    ##

    return wordList,apart,Word_Basic