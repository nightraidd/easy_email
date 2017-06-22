#coding:utf-8
import smtplib,os,re,time
from threading import *
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from email.mime.multipart import MIMEMultipart
qq_mail=[]
qq_name=[]
qq_number=os.path.join(os.getcwd(),"qq_number.txt")
email_content=os.path.join(os.getcwd(),"email_content.txt")
picture_abspath_dir=os.path.join(os.getcwd(),"email_picture")
with open(qq_number,"r")  as fb:              #打开并读取含有qq号和姓名的文件
	for line in fb:
		if re.findall(r"^#",line):      #看开头是否被#注释掉，如果注释掉就跳过读取
			continue        
		line_left=re.split(r"\s+#",line)#正则表达式分开邮箱和姓名
		qq_mail.append(line_left[0])    #用列表存储邮箱地址
		qq_name.append(line_left[1].strip("\n"))#用列表存储姓名并去掉后面的回车
length=len(qq_mail)                             #得到列表的长度就表示有几行信息，后面开线程时要用到
with open(email_content,"r") as fc: #读取要写入邮件的内容
		content=fc.read()                              #把读取的内容存入一个字符串变量
def send_picture(picture_abspath,msg,picture_name,hz):
	lock=Lock()
	time1=time.time()
	#lock.acquire()
	with open (picture_abspath,"rb") as f:
		mime = MIMEBase('image',hz, filename=picture_name)
		mime.add_header('Content-Disposition', 'attachment', filename=picture_name)
		mime.add_header('Content-ID', '<0>')
		mime.add_header('X-Attachment-Id', '0')
		mime.set_payload(f.read())
		encoders.encode_base64(mime)
		msg.attach(mime)
	time2=time.time()
	print("Sending %s to(%fs)..."%(picture_name,time2-time1))
	#lock.release()
def send_email(object_mail,object_name,content,title,picture_abspath_dir):       #发送邮件的具体函数
	lock.acquire()                                     #获取线程锁
	tz=[]
	hz_list=[]
	abspath_pic_list=[]
	time1=time.time()                                  #获取初始时间
	msg=MIMEMultipart()
	msg.attach(MIMEText("Hello %s！\n %s"%(object_name,content),"plain","utf-8")) #初始化邮件内容
	from_addr="xxxxxxxxx.com"                                #发送邮件的账号
	passwd="xxxxxxxx"                                             #发送邮件账号的密码
	smtp_server="smtp.163.com"                                     #smtp服务器   
	msg['From'] = 'Night_Raid <%s>' % from_addr                    #设置发件人信息
	msg['To'] = '%s<%s>' % (object_name,object_mail)               #设置收件人信息 
	msg['Subject'] =title                       #设置邮件的标题
	server=smtplib.SMTP(smtp_server)                               #初始化右键服务器对象
	picture_list=os.listdir(picture_abspath_dir)
	for pic in picture_list:
		if re.findall(r"db$",pic):
			continue	
		else:
			abspath_pic_list.append(os.path.join(picture_abspath_dir,pic))
			hz=re.findall(r"\.(.*$)",pic)
			hz_list.append(hz[0])
	#server.set_debuglevel(1)
			#显示邮件发送的详细信息并调试bug
	if "Thumbs.db" in picture_list:
		picture_list.remove("Thumbs.db")
	print(picture_list)
	if picture_list:
		t1=t2=t3=t4=t5=t6=t7=t8=t9=t10=t11=t12=t13=t14=t15=0
		t=["t1","t2","t3","t4","t5","t6","t7","t8","t9","t10","t11","t12","t13","t14","t15"]
		for i in range(len(abspath_pic_list)):
			t[i]=Thread(target=send_picture,args=(abspath_pic_list[i],msg,picture_list[i],hz_list[i]))
			tz.append(t[i])
		for tx in range(len(abspath_pic_list)):
			tz[tx].start()
		for ty in range(len(abspath_pic_list)):
			tz[ty].join()
	else:
		pass
	server.login(from_addr,passwd)                                 #利用server对象登录第三方邮件服务               
	server.sendmail(from_addr,[object_mail],msg.as_string())       #开始发送邮件
	server.quit()                                                  #关闭发送服务
	time2=time.time()                                              #获取邮件发送时间
	print("Has Sent Eamil to %s(%fs)..."%(object_name,time2-time1))
	lock.release()                                                 #释放线程锁
if __name__=="__main__":
	lock=Lock()                                                   #初始化线程锁对象
	t1=t2=t3=t4=t5=t6=t7=t8=t9=t10=t11=t12=t13=t14=t15=0          #初始化变量为后面批量创建线程用
	t=["t1","t2","t3","t4","t5","t6","t7","t8","t9","t10","t11","t12","t13","t14","t15"]#最大支持同时发送15封邮件
	tz=[]
	title=input("Please Input Email's Title:")
	for i in range(length):   # 批量创建线程
		t[i]=Thread(target=send_email,args=(qq_mail[i],qq_name[i],content,title,picture_abspath_dir))
		tz.append(t[i])
	for tx in range(length):  #批量开始线程
		tz[tx].start() 
	for ty in range(length):  #批量等待线程由于有线程锁，作用跟for循环无异
		tz[ty].join()







