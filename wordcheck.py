##导入包，其中cnradical用来得到字的偏旁部首。
from xpinyin import Pinyin
import re
from cnradical import Radical, RunOption
import os

##判断是否是中文敏感词
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
##处理一行的文本，得到相应的偏旁部首拆分替换的敏感词内容
##输入：偏旁部首敏感词表，行内容line_copy2,初始敏感词表Word_Basic(用于匹配敏感词原本内容)
def dealRadical(radicallist,line_copy2,Word_Basic):
    ans=''
    ##遍历每个敏感词的所有偏旁部首
    for word in radicallist:
        flag = True
        ##设置flag，循环确认行中的敏感词被全部输出
        while flag:
            flag=False
            ##正则最小匹配寻找敏感词首尾的偏旁部首之间的内容
            m=re.search(word[0]+r'.*?'+word[word.__len__()-1],line_copy2)
            ##由于得到的首尾偏旁部首可能不包括敏感词的全部内容，比如：邪教的偏旁是：阝攵，我们期望得到的是牙攵之间的全部内容
            ##所以需要对得到的内容长度进行判断
            if m!=None:
                ##当长度正好是初始敏感词长度的两倍，则那正好是所需的最远两个偏旁，之间以得到的re.search下标输出
                if m.end()-m.start()==2*word.__len__():
                    ##遍历确认属于拿个初始敏感词
                    for h in Word_Basic:
                        if ischinese(h) and find(h)==word:
                            ##输出格式（）
                            ##删除行中输出内容
                            ans=ans+("<"+h+ ">"+line_copy2[m.start():m.end()]+"\n")
                    line_copy2 = re.sub(line_copy2[m.start():m.end()],'',line_copy2,1)
                    ##当长度正好是初始敏感词长度的两倍减一，则需要输出前一个字符或者后一个字符
                elif m.end()-m.start()==2*word.__len__()-1:
                    ##确认前一或后一字符的偏旁部首是否是本身，如果是则确认是已被拆分的汉字，即是需要输出的内容
                    if [radical.trans_ch(ele) for ele in line_copy2[m.end()+1]]==line_copy2[m.end()+1]:
                        for h in Word_Basic:
                            if ischinese(h) and find(h) == word:
                                ##输出格式（）
                                ##删除行中输出内容
                                ans=ans+("<"+h+ ">"+line_copy2[m.start():m.end()+1]+'\n')
                        line_copy2 = re.sub(line_copy2[m.start():m.end()+1], '',line_copy2,1)
                    else:
                        for h in Word_Basic:
                             if ischinese(h) and find(h)==word:
                                 ##输出格式（）
                                 ##删除行中输出内容
                                 ans=ans+("<"+h+">"+line_copy2[m.start()-1:m.end()]+'\n')
                        line_copy2 = re.sub(line_copy2[m.start()-1:m.end()], '', line_copy2,1)
                ##除去以上两种情况，剩下的情况是第一个字取到右边的拆分字，最后一字取到左边拆分字
                else:
                    for h in Word_Basic:
                        if ischinese(h) and find(h)==word:
                            ans=ans+("<"+ h+ ">"+line_copy2[m.start()-1:m.end() + 1]+'\n')
                            line_copy2 = re.sub(line_copy2[m.start()-1:m.end()+1], '', line_copy2,1)
            ##research结果为空则之间跳出循环
            else:
                break
            ##判断是否还有要输出的敏感词
            if re.search(word[0] + r'.*?' + word[word.__len__() - 1], line_copy2)!=None:
                flag=True
    ##返回该行中需要输出的全部内容
    if ans != '':
        return ans
    else:
        return None
##搜寻形如：原型：邪教，首字符替换：x教，全字符替换：xiejiao，单字全拼音替换：xie教等。
def dealelse(line,wordList,line_copy,Word_Basic):
    ans=''
    flag=1
    while flag:
        for word in wordList:
            len=word.__len__()
            ##设置是否存在敏感词输出标记
            ifhasput=0
            ##遍历行每个字符
            for j in range(line_copy.__len__()):
                ##当遇到与当前敏感词首字一样的拼音
                if p.get_pinyin(line_copy[j], '')==p.get_pinyin(word[0], ''):
                    ##设置第一个输出字符下标
                    start=j
                    ##原文中全部该输出内容的长度
                    orglength = 1
                    ##匹配敏感词的长度
                    wordlength= 1
                    for f in range(start + 1, line_copy.__len__()):
                        ##遇到空格内容怎输出内容总长加1
                        if line_copy[f]== ' ':
                            orglength= orglength + 1
                        ##如果遇到匹配的拼音不同，则不是我们要找到敏感词，退出
                        elif  p.get_pinyin(line_copy[f], '').lower()!= p.get_pinyin(word[wordlength], '').lower():
                            break
                        ##遇到对应的拼音，增加总长与敏感词长度
                        elif p.get_pinyin(line_copy[f], '').lower()==p.get_pinyin(word[wordlength], '').lower():
                            wordlength= wordlength + 1
                            orglength= orglength + 1
                            ##当敏感词长度与当前遍历的敏感词长度一样则确定可以输出
                            if wordlength==len:
                                ifhasput=1
                                break
                if ifhasput==1 :break
            if ifhasput==1:
                #接下来判断当前敏感词与初始敏感词的匹配
                #遍历初始词表

                for aword in Word_Basic:
                    index1 = 0
                    index2 = 0
                    g=''
                    g=p.get_pinyin(aword, '')
                    ##与初始的全拼一致
                    if g == p.get_pinyin(word, ''):
                        ans=ans+("<"+str(aword)+">")
                        break
                    ##与初始的首字符替换一致
                    for num in range(aword.__len__()):
                        m = p.get_initials(aword, '')
                        t = re.sub(m[num], p.get_pinyin(aword[num], ''), m)
                        if t.lower()==p.get_pinyin(word,'').lower():
                            index1=1
                            ans=ans+("<"+ aword+ ">")

                            break
                    if index1==1:
                        break
                    else:
                        ##与初始的混合拼音一致
                        for everyword in aword:
                            pinyin_low=re.sub(everyword, p.get_initial(everyword, '').lower(), aword)
                            if p.get_pinyin(pinyin_low,"")==p.get_pinyin(word,'').lower():
                                index2=1
                                ans=ans+("<"+ aword+ ">")

                                break
                    if index2==1:
                        break
                ##由得到的输出内容的初始下标与结尾下标依次输出每个字符
                ##然后删去行中对应的内容
                for s in range(start, start + orglength - 1):
                    ans=ans+(line[s])
                ans=ans+(line[start + orglength - 1]+'\n')
                line = line[0:start] + line[start + orglength:line.__len__()]
                line_copy= line_copy[0:start] + line_copy[start + orglength:line_copy.__len__()]
        ##判断是否还有需要输出的敏感词，没有则退出循环
        for aWord in Word_Basic:
            d = re.sub(' ', '', line_copy)
            d = p.get_pinyin(d, '')
            if re.search(p.get_pinyin(aWord, ''), d) == None:
                flag = 0
            else:
                flag = 1
                break
    ##返回该行中需要输出的全部内容
    if ans!='':
        return ans
    else:
        return None


lineNumber=0   ##设置行数变量
m=[]
fileorgname=input("输入敏感词文件，待检测文本，答案路径：")##
fileorgname=fileorgname.split(" ")
fileorg=open(fileorgname[1],encoding='utf8')##打开原文文件
filewords=open(fileorgname[0],encoding='utf8')##打开敏感词表
ans=open(fileorgname[2],mode='w')##设置答案路径
p=Pinyin()##拼音声明
radical = Radical(RunOption.Radical)##字符声明
wordlist,apartlist,basiclist=preword(filewords)##得到敏感词派生表，敏感词偏旁部首表，敏感词初始表
num=0##文中敏感词总量
##遍历待检测文件的每行
for line in fileorg.readlines():
    line_copy=line##复制
    lineNumber= lineNumber + 1##行数加1
    ##去掉行中的全部非汉字英文字符，用空格替换
    ##并将全部英文转为小写
    line_copy = re.sub(r'[’!"#$\s%&\'()*￣ ￣ ╭╯□╰！@#￥%…☆&*·*+,-./:;<=>?@，0123456789。?★、…【】《》？“”‘’！\[\\\]^_`{|}~：]', ' ', line)
    line_copy = line_copy.lower()
    ##分别得到ans1：偏旁部首替换敏感词的输出内容
    ##      ans2：其他替换输出内容
    ans1=dealRadical(apartlist,line_copy,basiclist)
    ans2=dealelse(line,wordlist,line_copy,basiclist)
    ##按格式输出所有非空ans
    if ans1!=None:
        for a in ans1.split('\n'):
            if a!='':
                ans.write("Line："+str(lineNumber)+a+'\n')
                num+=1
    ##按格式输出所有非空ans
    if ans2!=None:
        for a in ans2.split('\n'):
            if a !='':
                ans.write("Line："+str(lineNumber)+a+"\n")
                num+=1
##关闭文件
fileorg.close()
filewords.close()
ans.close()
#在行首加入total显示总数
with open(fileorgname[2], 'r+') as f:
    content = f.read()
    f.seek(0, 0)
    f.write('Total：'+str(num)+'\n'+content)
print("敏感词检测完成，总共出现",num,"次敏感词")





