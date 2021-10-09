from Init import p
import re
def dealelse(line,wordList,line_copy,Word_Basic):
    ans=''
    for word in wordList:

        count = 0##循环次数计数
        flag = 1##循环标记
        while flag:
            ##判断是否还有需要输出的敏感词，没有则退出循环
            line_noblank = re.sub(' ', '', line_copy)
            line_noblank = p.get_pinyin(line_noblank, "")
            if re.search(p.get_pinyin(word, '').lower(), line_noblank) == None:
                flag =0
                break
            else:
                flag = 1
            if flag==1 and count>5:
                flag=0
                break
            count=count+1
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
                    g=p.get_pinyin(aword,"")
                    ##与初始的全拼一致
                    if g == p.get_pinyin(word, '') or word==p.get_initials(aword,'').lower():
                        ans=ans+(" <"+str(aword)+"> ")
                        break
                    ##与初始的首字符替换一致
                    for num in range(aword.__len__()):
                        m = p.get_initials(aword, '')

                        t = re.sub(m[num], p.get_pinyin(aword[num], ''), m)
                        if t.lower()==p.get_pinyin(word,'').lower():
                            index1=1
                            ans=ans+(" <"+ aword+ "> ")

                            break
                    if index1==1:
                        break
                    else:
                        ##与初始的混合拼音一致
                        for everyword in aword:
                            pinyin_low=re.sub(everyword, p.get_initial(everyword, '').lower(), aword)
                            if p.get_pinyin(pinyin_low,"")==p.get_pinyin(word,'').lower():
                                index2=1
                                ans=ans+(" <"+ aword+ "> ")

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

    ##返回该行中需要输出的全部内容
    if ans!='':
        return ans
    else:
        return None