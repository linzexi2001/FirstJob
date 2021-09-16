import re
from Init import ischinese, find,radical
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
                            break
                    line_copy2 = re.sub(line_copy2[m.start():m.end()],'',line_copy2,1)
                    ##当长度正好是初始敏感词长度的两倍减一，则需要输出前一个字符或者后一个字符
                elif m.end()-m.start()==2*word.__len__()-1:

                    r=''
                    for s in [radical.trans_ch(ele) for ele in line_copy2[m.start()-1]]:
                        r=r+s
                    ##确认前一或后一字符的偏旁部首是否是本身，如果是则确认是已被拆分的汉字，即是需要输出的内容
                    if r==line_copy2[m.start()-1]:

                        for h in Word_Basic:
                            if ischinese(h) and find(h) == word:
                                ##输出格式（）
                                ##删除行中输出内容
                                ans=ans+("<"+h+ ">"+line_copy2[m.start()-1:m.end()]+'\n')
                                break
                        line_copy2 = re.sub(line_copy2[m.start()-1:m.end()], '',line_copy2,1)
                    else:
                        for h in Word_Basic:

                             if ischinese(h) and find(h)==word:

                                 ##输出格式（）
                                 ##删除行中输出内容
                                 ans=ans+("<"+h+">"+line_copy2[m.start():m.end()+1]+'\n')
                                 break
                        line_copy2 = re.sub(line_copy2[m.start():m.end()+1], '', line_copy2,1)
                ##除去以上两种情况，剩下的情况是第一个字取到右边的拆分字，最后一字取到左边拆分字
                else:
                    for h in Word_Basic:
                        if ischinese(h) and find(h)==word:
                            ans=ans+("<"+ h+ ">"+line_copy2[m.start()-1:m.end() + 1]+'\n')
                            line_copy2 = re.sub(line_copy2[m.start()-1:m.end()+1], '', line_copy2,1)
                            break
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