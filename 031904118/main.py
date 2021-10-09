from xpinyin import Pinyin
import re
from Init import preword
from radicaltest import dealRadical
from mixtest import dealelse
import sys
def main():
    try:
        lineNumber=0   ##设置行数变量
        fileorg=open(sys.argv[2],encoding='utf8')##打开原文文件
        filewords=open(sys.argv[1],encoding='utf8')##打开敏感词表
        ans=open(sys.argv[3],mode='w',encoding='utf8')##设置答案路径
        wordlist,apartlist,basiclist=preword(filewords)##得到敏感词派生表，敏感词偏旁部首表，敏感词初始表
        num=0##文中敏感词总量
        ##遍历待检测文件的每行
        for line in fileorg.readlines():
            lineNumber= lineNumber + 1##行数加1
            ##去掉行中的全部非汉字英文字符，用空格替换
            ##并将全部英文转为小写
            line_copy = re.sub(r'[’!"#$\s%&\'()*￣ ￣ ╭╯□╰！@#￥%…☆&*·*+,-./:;<=>?@，0123456789。?★、…【】《》？“”‘’！\[\\\]^_`{|}~：]', ' ', line)
            line_copy = line_copy.lower()
            ##分别得到ans1：偏旁部首替换敏感词的输出内容
            ##      ans2：其他替换输出内容
            ans1=dealRadical(apartlist,line_copy,basiclist)
            ans2=dealelse(line,wordlist,line_copy,basiclist)
            if ans1 != None:
                for a in ans1.split('\n'):
                    if a != '':
                        ans.write( "\n"+"Line" + str(lineNumber)+ ":"+ a )
                        num += 1
            ##按格式输出所有非空ans
            if ans2 != None:
                for a in ans2.split('\n'):
                    if a != '':
                        ans.write('\n'+"Line" + str(lineNumber)+ ":"+ a  )
                        num += 1
        ##关闭文件
        fileorg.close()
        filewords.close()
        ans.close()
        #在行首加入total显示总数
        with open(sys.argv[3], 'r+',encoding='utf8') as f:
            content = f.read()
            f.seek(0, 0)
            f.write('Total: '+str(num)+content)
        ans.close()
        print("敏感词检测完成，总共出现",num,"次敏感词")
    except :
        print("请输入正确的文件路径：[敏感词文件] [待检测文件] [答案]")
if __name__=='__main__':
    main()
