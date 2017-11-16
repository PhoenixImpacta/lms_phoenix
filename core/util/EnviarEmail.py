import smtplib

def enviarEmail(para, mensagem):
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    smtp.login('michael.jordan.java@gmail.com', 'c0r1ng41533')

    de = 'michael.jordan.java@gmail.com'
    print("-------",para)
    para = para
    smtp.sendmail(de, para, mensagem)
    smtp.quit()



'''
'lucasrodriguescirino@outlook.com', 'adilsonaraujo308@gmail.com',
            'hborges9294@gmail.com', 'enio.ferreira.jr@gmail.com' 
'''