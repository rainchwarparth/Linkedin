from selenium import webdriver  
import time
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import calendar
import datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta
import streamlit as st
import base64
from diver import *
 
st.title('LINKEDIN RECURITER INDIVDUAL PROFILES DATA EXTRACTION')


def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    return f'<a href="data:file/csv;base64,{b64}" download="output.csv">Download csv file</a>'

with st.form("my_form"):

        links = st.text_input("Enter Links:")
        submitted_new = st.form_submit_button("EXTRACT")
        if submitted_new:
            home_url = get__url()
            link_list = links.split(',')

            sleep(10)
            sourc_main = []
            for i in range(0,len(link_list)):
                gotourl(link_list[i])
                time.sleep(5)
                execute_script()
                sleep(3)
                src_main = src_code()
                sourc_main.append(src_main)
                sleep(2)


            email_l1 = []
            contact_l2 = []
            name_l3 = []
            pl_l4 = []
            com_l5 = []
            experience = []
            for i in range(0,len(sourc_main)):
                soup_main = BeautifulSoup(sourc_main[i])
                name = soup_main.find('title').text
                if name != 'LinkedIn Member':
                    name_l3.append(name)
                    details = soup_main.find_all('li',{'class':'contact-info__list-item'})
                    t1 = []
                    t2 = []
                    for s in range(0,len(details)):
                        spans = details[s].find('span')
                        if spans != None:
                            if 'contact-info__email-address' in str(spans):
                                email = spans.text
                                t1.append(email)
                            if 'data-live-test-contact-phone' in str(spans):
                                cont = spans.text
                                t2.append(cont)
                        else:
                            t1.append([])
                            t2.append([])
                    email_l1.append(t1)
                    contact_l2.append(t2)
                    public_link = soup_main.find('a',{'class':'personal-info__link'})
                    pl = public_link.find('span',{'aria-hidden':'true'}).text.strip()
                    pl_l4.append(pl)

                    div = soup_main.find_all('div',{'class':"""expandable-list expandable-stepper background-section__container expandable-list-profile-core"""})
                    liii = div[0].find_all('li')
                    val = liii[0]
                    lat_com = val.find_all('dd',{'class':'background-entity__summary-definition--subtitle'})
                    com_grp = val.find_all('strong',{'class':'t-16 grouped-position-entity__company-name'})
                    if lat_com != []:
                        if 'position-item__company-link' in str(lat_com[0]):
                            com = lat_com[0].find('a',{'class':'position-item__company-link'}).text.strip()
                            com_l5.append(com)
                        elif '<dd class="background-entity__summary-definition--subtitle" data-test-position-entity-company-name="">' in str(lat_com):
                            strip_1 = """<dd class="background-entity__summary-definition--subtitle" data-test-position-entity-company-name="">"""
                            s_2 = "\n"
                            lsname = str(lat_com[0]).strip(strip_1).strip()
                            lsnamee = str(lsname[0]).strip(s_2)
                            com_l5.append(lsnamee)
                    elif com_grp !=[]:      
                        com_l5.append(com_grp[0].text)
                    else:
                        t = []
                        com_l5.append(t)

                    #experience
                    div_va = soup_main.find_all('div',{'class':"""background-section experience-card"""})
                    if len(div_va) != 0 :
                        li = div_va[0].find_all('time')
                        exp = []
                        if len(li)/2 != 0:
                            for j in range(0,len(li)):
                                val = str(li[j]).split('<time>')
                                v_2 = str(val[1]).rsplit('</time>')
                                exp.append(v_2[0])
                            exp.insert(1,'Present')
                        experience.append(exp)
                    else:
                        exp = []
                        experience.append(list(exp))

            
            gotourl(home_url)
            p_link = []
            for i in range(0,len(pl_l4)):
                link = pl_l4[i].split('.',1)
                lll_link = 'https://www.' + link[1] + '/'
                p_link.append(lll_link)
                
            main = []
            for i in range(0,len(experience)):
                temp =[]
                for j in range(0,len(experience[i]),2):
                    val = experience[i][j:j+2]
                    temp.append(val)
                main.append(temp)

            currentDate = datetime.date.today()
            currentMonthName = calendar.month_name[currentDate.month]

            z = str(currentMonthName[0:3]) +' '+ str(currentDate.year)

            for i in range(0,len(main)):
                for j in range(0,len(main[i])):
                    if len(main[i][j]) < 2 :
                        main[i].remove(main[i][j])
                    
            for i in range(0,len(main)):
                for j in range(0,len(main[i])):
                    if main[i][j][1] == 'Present':
                        main[i][j][1] = z

            for i in range(0,len(main)):
                for j in range(0,(len(main[i]))):
                    if len(main[i][j][0]) == 4 :
                        main[i][j][0] = 'Jan ' + main[i][j][0]
                    if len(main[i][j][1]) == 4:
                        main[i][j][1] = 'Jan ' + main[i][j][1]
                        
            exp_count = []
            for i in range(0,len(main)):
                nil = 0
                mon_nil = 0
                for j in range(0,len(main[i])):
                    val = (parser.parse(main[i][j][1]).year) - (parser.parse(main[i][j][0]).year)
                    if val < 0:
                        val = val * (-1)
                    mon_val = (parser.parse(main[i][j][1]).month) - (parser.parse(main[i][j][0]).month)
                    if mon_val < 0 :
                        mon_val = mon_val * (-1)
                    nil = nil + val
                    mon_nil = mon_nil + mon_val
                total = nil*12 + mon_nil
                yrs = int(total/12) 
                mon = int(total % 12)
                if mon < 10:
                    mon = "{0:0=2d}".format(mon) 
                output = str(yrs)+'.'+str(mon)
                exp_count.append(float(output))
                


            data = {'Public Link':p_link,
                    'Name': name_l3,
                    'Email':email_l1,
                    'Contact':contact_l2,
                    'Current Company':com_l5,
                    'Experience_count': exp_count
                }

            df = pd.DataFrame(data)
            st.dataframe(data=df)
            st.markdown(get_table_download_link(df), unsafe_allow_html=True)
