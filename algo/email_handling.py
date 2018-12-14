#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 18:03:40 2017

@author: hiub
"""

# =============================================================================
# 
# =============================================================================
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders



import imaplib, email, os
import re
import time
import datetime
import random
import csv
import unidecode

import pandas                                       as pd


from email.header                                   import decode_header
from email.parser                                   import Parser
from bs4                                            import BeautifulSoup


# =============================================================================
# 
# =============================================================================
def email_verification_adress(email):
    addressToVerify = email.strip().lower()
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)
    is_valid = 0
    if match != None: 
        is_valid = 1
    return is_valid
    


    
"""
def check_latest_email_id(username, password):    
    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login(username, password)
    mail.select('Inbox')
    typ, data = mail.uid('search', None, 'ALL')
    
    latest_email_uid = data[0].split()[-1]
    result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
    raw_email = data[0][1]

    emailBody = raw_email
    headers = Parser().parsestr(emailBody)
    email_sender = headers['from']
    email_subject = headers['Subject']
    try:
        email_sender = email_sender.split('<', 1)[1].split('>')[0]
    except IndexError:
        email_sender = email_sender
    message_id = headers['Message-ID']
                    
    return emailBody, email_subject, message_id, email_sender
""" 

def email_get_latest_attachments(save_dir='../dataset/local/pdf'):
    username            = 'auchan.cgv'
    password            = 'pretorien'
    mail                = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login(username, password)
    mail.select('Inbox')
    typ, data           = mail.uid('search', None, 'ALL')
    fileType            = 'nan'
    attached_pdf        = 0
    
    if(data[0]!=''):
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
    
        emailBody = raw_email
        headers = Parser().parsestr(emailBody)
        email_sender = headers['from']
        email_subject = headers['Subject']
        try:
            email_sender = email_sender.split('<', 1)[1].split('>')[0]
        except IndexError:
            email_sender = email_sender
        message_id = headers['Message-ID']
        
        mail_m = email.message_from_string(emailBody)
        filePath = 'nan'
        for part in mail_m.walk():
            if part.get_content_maintype() == 'multipart':
                # print part.as_string()
                continue
            if part.get('Content-Disposition') is None:
                # print part.as_string()
                continue
            fileName = part.get_filename()
            fileName = decode_header(fileName)[0][0]
            fileType = part.get_content_type()
    
            if bool(fileName):
                filePath = os.path.join(save_dir,fileName)
                
                if fileName[-3:].lower() == 'pdf':
                    attached_pdf = attached_pdf + 1
                if not os.path.isfile(filePath) :
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
    
        result, data = mail.uid('STORE', latest_email_uid, '+X-GM-LABELS' ,'processed')        
        result, data = mail.uid('STORE', latest_email_uid, '+FLAGS', '\\Deleted')   
        
        flag_new_email = 1

        
    else:
        emailBody = email_subject = message_id = latest_email_uid = email_sender = filePath = fileType = attached_pdf = 'nan'
        flag_new_email = 0
        
    return flag_new_email, [emailBody, email_subject, message_id, latest_email_uid, email_sender, filePath, fileType, attached_pdf]
    

#%%
def email_send_without_attachments(toaddr='mdesmarez@gmail.com', body_message='', subject='Alert', address_from="auchan.cgv@gmail.com", address_from_password='pretorien'):
    """
    INPUT   : adress mail / array image / text message str
    OUTPUT  :
    """
    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    from email.MIMEBase import MIMEBase
    from email import encoders
    import os
     
    
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('mixed')
    msg['From'] = address_from
    msg['To'] = toaddr.strip().lower()
    msg['Subject'] = subject
    
    
    body_message = body_message.replace('\n','<br>')


    # Create the body of the message (a plain-text and an HTML version).
    html = body_message


    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
     
    # Send the message via local SMTP server.
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(address_from, address_from_password)
    server.sendmail(address_from, toaddr, msg.as_string())
    server.quit()
    
#%%
def email_send_html_with_attachment(toaddr='mdesmarez@gmail.com', body_message='', subject='Alert', filename_path='', address_from="auchan.cgv@gmail.com", address_from_password='pretorien'):
    """
    INPUT   : adress mail / array image / text message str
    OUTPUT  :
    """
    fromaddr        = "auchan.cgv@gmail.com"
    password        = 'pretorien'
    
    
    # Create message container - the correct MIME type is multipart/alternative.
    msg             = MIMEMultipart('mixed')
    msg['From']     = fromaddr
    msg['To']       = toaddr
    msg['Subject']  = subject

    body_message = body_message.replace('\n','<br>')

    # Create the body of the message (a plain-text and an HTML version).
    html = body_message

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(html, 'html')



    filename        = filename_path.split('/')[-1]
    attachment      = open(filename_path, "rb")
    part2           = MIMEBase('application', 'octet-stream')
    part2.set_payload((attachment).read())
    encoders.encode_base64(part2)
    part2.add_header('Content-Disposition', "attachment; filename= %s" % filename)


    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

     
    # Send the message via local SMTP server.
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(address_from, address_from_password)
    server.sendmail(address_from, toaddr, msg.as_string())
    server.quit()


#%%
def email_send_with_attachments(toaddr='mdesmarez@gmail.com', image='', body_message='', date_receipt=''):
    """
    INPUT   : adress mail / array image / text message str
    OUTPUT  :
    """
    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    from email.MIMEBase import MIMEBase
    from email import encoders
    import os
     
    fromaddr = "auchan.cgv@gmail.com"
    password = 'pretorien'
    
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('mixed')
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "EATSY 0.4 - Ticket du " + str(date_receipt)
    
    #import html file
    cur_dir_here = os.path.split(os.path.realpath(__file__))[0]
    file = open(cur_dir_here + '/./eatsy_mail_model.html', "r")
    html_content = file.read()
    #adapt the content
    body_message = body_message.replace('\n','<br>')
    body_message_list = body_message.split('<<>>')
    body_message_date = body_message_list[0]
    body_message_category = body_message_list[1]
    #body_message_article = body_message_list[2]
    #body_message_pnns = body_message_list[3]
    body_message_recipe = body_message_list[2]
    html_content = html_content.replace('&lt;&lt;date&gt;&gt;',body_message_date)
    #html_content = html_content.replace('&lt;&lt;articles&gt;&gt;',body_message_article)
    #html_content = html_content.replace('&lt;&lt;pnns&gt;&gt;',body_message_pnns)
    html_content = html_content.replace('&lt;&lt;category&gt;&gt;',body_message_category)
    html_content = html_content.replace('&lt;&lt;recipe&gt;&gt;',body_message_recipe)


    # Create the body of the message (a plain-text and an HTML version).
    html = html_content


    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(html, 'html')

    image = Image.fromarray(image)
    cur_dir_here = os.path.split(os.path.realpath(__file__))[0]
    path_img_save = cur_dir_here + '/../../solution/attachment/attachment.jpg'
    image.save(path_img_save)
    filename = "attachment.jpg"
    attachment = open(path_img_save, "rb") 
    part2 = MIMEBase('application', 'octet-stream')
    part2.set_payload((attachment).read())
    encoders.encode_base64(part2)
    part2.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
     
    # Send the message via local SMTP server.
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()
    
#%%
# =============================================================================
#     
# =============================================================================
# =============================================================================
# 
# =============================================================================
def remove_accent(text):
    if(type(text) == unicode):
        text    =   unidecode.unidecode(text)
    else:
        text    =   unidecode.unidecode(text.decode('utf-8'))
    return text
    

def unidecode_all(string):
    if(type(string) == unicode):
        string = string.encode('utf-8') 
    return string


def substring_indexes(substring, string):
    """ 
    Generate indices of where substring begins in string

    >>> list(find_substring('me', "The cat says meow, meow"))
    [13, 19]
    """
    last_found = -1  # Begin at -1 so the next position to search from is 0
    while True:
        # Find next index of substring, by starting after its last known position
        last_found = string.find(substring, last_found + 1)
        if last_found == -1:  
            break  # All occurrences have been found
        yield last_found
        
def log_writer_email(solution, email_from, email_date, email_subject, email_body, email_raw, list_filename, list_save_dir_id, save_dir, is_thread):    
    log_email_file = save_dir + "log_email_" + solution + ".csv"
        
    if(os.path.isfile(log_email_file) == False):
        csvwriter = csv.writer(open(log_email_file, "ab"))
        csvwriter.writerow(["date","solution","email_from","email_date","email_subject","email_body", "list_filename","list_save_dir_id","is_thread"])
    else:
        csvwriter = csv.writer(open(log_email_file, "ab"))

    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    solution        = unidecode_all(solution)
    email_from      = unidecode_all(email_from)
    email_subject   = unidecode_all(email_subject)
    email_body      = unidecode_all(email_body)

    row = [date]
    row.extend([solution])
    row.extend([email_from])
    row.extend([email_date])
    row.extend([email_subject])
    row.extend([email_body])
#    row.extend([email_raw])
    row.extend([list_filename])
    row.extend([list_save_dir_id])
    row.extend([is_thread])

    csvwriter.writerow(row)

# =============================================================================
#     
# =============================================================================
def email_move_directory(PARAMETER_EMAIL, email_uid, folder='receipt_done'):
    username, password, provider = PARAMETER_EMAIL
    mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    mail.login(username, password)
    mail.select('Inbox')
    apply_lbl_msg = mail.uid('COPY', email_uid, folder)
    mov, data = mail.uid('STORE', email_uid , '+FLAGS', '(\Deleted)')
    mail.expunge()

    

def email_reading(PARAMETER_EMAIL, solution, recover_x_emails, folder='Inbox', list_ext_out= ['xxx'], save_dir='./', put_flag=False):
    
    username, password, provider = PARAMETER_EMAIL
    
    mail = imaplib.IMAP4_SSL(provider, 993)
    mail.login(username, password)
    mail.select(folder)
    typ, data = mail.uid('search', None, 'ALL')
    save_dir_id = save_dir + solution
    os.system('mkdir -p ' + save_dir_id)
    df_email = pd.DataFrame()
                    
    if(data[0] != ''):
        list_data = data[0].split()
        list_data.reverse()
        list_data_batch  = []
        ###limit number of email read
        list_data_limit = list_data[:recover_x_emails]
        for i, item in enumerate(list_data_limit):
            list_data_batch.append(item)
            email_uid           = item.split()[-1]
            result, datamail    = mail.uid('fetch', email_uid, '(RFC822)')
            raw_email           = datamail[0][1]
            emailBody           = raw_email
            headers             = Parser().parsestr(emailBody)
            email_from          = headers['From']
            email_to            = headers['To']
            email_date          = headers['Date']
            email_content_type  = headers['Content-Type']
            email_id            = headers['Message-ID']
            email_subject       = headers['Subject']
            email_thread_index  = headers['Thread-Index']
            email_references    = headers['References']
            email_reply         = headers['In-Reply-To']
            
#            a = headers.items()
            
            
            
            ### identify if email is single message or part of thread
            """
            email_from_modif    = email_from.split('<')[-1][:-1]
            try:
                typz, data_sub      = mail.uid('search', None, '(SUBJECT "' + email_subject[5:] +'")')
            except:
                data_sub = ['']
            try:
                typz, data_from    = mail.uid('search', None, '(FROM "' + email_from_modif + '")')
            except:
                data_from = ['']
            lst3 = list(set(data_sub[0].split(' ')) & set(data_from[0].split(' ')))

            if data_sub != [''] and len(lst3) == 1:
                print ('only mail')
                is_thread = 0
            else:
                print ('not know or thread')
                is_thread = 1
            """
            
            if email_references == None or email_reply == None:
                print ('only mail')
                is_thread = 0
            else:
                print ('not know or thread')
                is_thread = 1
        
        
            ### <!> ###
            is_thread = 0
            ### <!> ###
        
        
            ### decode multi subject
            email_subject_decode = ''
            for item in decode_header(email_subject):
                email_subject_decode = email_subject_decode + ' ' + item[0].strip()
            email_subject = email_subject_decode.strip()
            try:
                email_subject = email_subject.decode(item[1]).encode('utf-8')
            except:
                pass


#            ### find email from
#            if email_from == '<Veronique_Calvez@Praxair.com>':
#                break

            
            ### Save attached file
            if save_dir != './':
                list_filename       = []
                list_save_dir_id    = []
                mail_m = email.message_from_string(emailBody)
                filePath = 'nan'
                email_body = ''
                for part in mail_m.walk():
                    if part.get_content_maintype() == 'text':
                        charset = part.get_content_charset()
                        email_body = ''
                        if charset is not None:    
                            if part.get_content_type() == 'text/plain':
                                email_body_bulk = unicode(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')
                
                            if part.get_content_type() == 'text/html':
                                email_body_bulk = unicode(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')
    
                                soup            = BeautifulSoup(email_body_bulk)
                                email_body      = soup.get_text()
                                email_body      = str(email_body.encode('utf-8'))
                                
    #                        if email_body_bulk.find('<body') != -1:
    #                            email_body_html = email_body_bulk[email_body_bulk.find('<body'):]
    #                            soup            = BeautifulSoup(email_body_html)
    #                            email_body      = soup.get_text()
    #                            email_body      = email_body.strip()
    #                            email_body      = str(email_body.encode('utf-8'))
    #                        else:
    #                            email_body      = email_body_bulk
    #                        
                            
                    
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue
                    fileName = 'null.png'
                    fileName = part.get_filename()
    #                print fileName
    
                    try:
                        fileNameTemp    = decode_header(fileName)
                        if fileNameTemp[0][1] == None:
                            fileName    = unidecode.unidecode(fileName)
                        else:
                            fileName    = fileNameTemp[0][0].decode(fileNameTemp[0][1]).encode('utf-8')
                        fileName        = unidecode.unidecode(fileName.decode('utf-8'))
                    ### for encoding == none
                    except:
                        pass
    
                    
                    if fileName is not None:
                        fileName = fileName.lower()
                        if len(fileName.split('.')) > 0:
                            fileExt  = fileName.split('.')[-1]
                            if bool(fileName) and ((fileExt in list_ext_out) == False):
                                unique_id   = str(random.randint(0,100000000)).zfill(11)
                                save_dir_id = save_dir + solution + '/' + unique_id
                                
                                os.system('mkdir -p ' + save_dir_id)
                                filePath = os.path.join(save_dir_id,fileName)
                                                                
                                if not os.path.isfile(filePath) :
                                    fp = open(filePath, 'wb')                                
                                    try:
                                        fp.write(part.get_payload(decode=True))
                                    except:
                                        pass                                
                                    fp.close()
                                list_filename.append(fileName)
                                list_save_dir_id.append(save_dir_id + '/' + fileName)
            else:
                list_filename       = []
                list_save_dir_id    = []
                
            try:
                a = email_body
            except:
                email_body = ''
                
            print(str(i+1) + ' emails saved')
            print i, item, email_subject, email_id
            log_writer_email(solution, email_from, email_date, email_subject, email_body, raw_email[:5000], list_filename, list_save_dir_id, save_dir + solution + '/', is_thread)            
            
            df_email_temp            = pd.DataFrame([[solution],[email_uid], [email_from], [email_date], [email_subject], [email_body], [list_filename], [list_save_dir_id], [is_thread]]).T
            df_email_temp.columns    = ['solution','email_uid','email_from', 'email_date', 'email_subject', 'email_body', 'list_filename', 'list_save_dir_id', 'is_thread']
            df_email                 = pd.concat([df_email, df_email_temp])
            
    else:
#        print 'Empty email folder'
        pass
        
    return df_email

#%%
def email_sending(PARAMETER_EMAIL, address_to, subject = '', html_message = '', attachment_path = ''):
    """
    INPUT   : adress mail / array image / text message str
    OUTPUT  :
    """
    
    USERNAME, PASSWORD, PROVIDER = PARAMETER_EMAIL

    
    # Create message container - the correct MIME type is multipart/alternative.
    msg             = MIMEMultipart('mixed')
    msg['From']     = USERNAME
    msg['To']       = address_to
    msg['Subject']  = subject

    # Record the MIME types of both parts - text/plain and text/html.
    part1           = MIMEText(html_message, 'html')
    msg.attach(part1)

    if attachment_path != '':
        filename        = attachment_path.split('/')[-1]
        attachment      = open(attachment_path, "rb")
        part2           = MIMEBase('application', 'octet-stream')
        part2.set_payload((attachment).read())
        encoders.encode_base64(part2)
        part2.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part2)

    # Send the message via local SMTP server.
    server          = smtplib.SMTP(PROVIDER, 587)
    server.starttls()
    server.login(USERNAME, PASSWORD)
    server.sendmail(USERNAME, address_to, msg.as_string())
    server.quit()