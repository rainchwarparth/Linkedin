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

def app():
    st.title('PUBLIC LINKEDIN SCRAPPER')

    def get_table_download_link(df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
        return f'<a href="data:file/csv;base64,{b64}" download="output.csv">Download csv file</a>'


    with st.form("my_form"):

        link = st.text_input('Enter filtered Linkedin link :')
        userid = st.text_input('Enter username :')
        pass_word = st.text_input('Enter password :',type="password")
        total_records_required = st.text_input('Enter total records required :')

        submitted_new = st.form_submit_button("EXTRACT")
        if submitted_new:

            # if int(total_records_required) < 50:
            #     req = 50
            # else:
            #     req = int(total_records_required)

            req = int(total_records_required)

            link_1 = link.rsplit('&',1)
            link_page_default = link_1[0] + '&page={}'

            rounded = ((round(req/10)*10 ) + 10)

            page_count = int(rounded/10)

            page_links = []
            for i in range(0, page_count):
                page_link = link_page_default.format(i + 1)
                page_links.append(page_link)

            diver()
            gotourl("https://www.linkedin.com/") #URL   
            find_element_xpath_click_send_keys("""//*[@id="session_key"]""",userid) #EMAIL
            find_element_xpath_click_send_keys("""//*[@id="session_password"]""",pass_word) #PASSWORD
            find_element_xpath_click("""//*[@id="main-content"]/section[1]/div/div/form/button""")

            implicitly_wait(10) #implicit wait for 10 seconds

            sleep(5)
            person_link = []
            for i in range(0,len(page_links)):
                gotourl(page_links[i])
                for j in range(1,11):
                    temp = '//*[@id="main"]/div/div/div/ul/li[{}]/div/div/div[2]/div[1]/div[1]/div/span[1]/span/a'.format(j)
                    person_link.append(find_element_xpath_get_attr(temp,'href'))

            individual_link = []
            for i in range(0,len(person_link)):
                text = person_link[i].split("?",1)
                fin_link = text[0] + '/'
                individual_link.append(fin_link)
                            
            selected_link = []
            for i in range(0,req):
                selected_link.append(individual_link[i])
                
            count_not_connection = 0    
            selected_list = []
            for i in range(0,len(selected_link)):
                if (selected_link[i] == 'https://www.linkedin.com/search/results/people/headless/'):
                    count_not_connection = count_not_connection + 1 
                else:
                    selected_list.append(selected_link[i])

            source_main = []
            source_skill = []
            source_experience = []
            for i in range(0,len(selected_list)):
                gotourl(selected_list[i])
                execute_script()
                src_main = src_code()
                source_main.append(src_main)
                implicitly_wait(10) #implicit wait for 10 seconds

                gotourl('{}'.format(selected_list[i] + 'details/skills/' ))
                sleep(2.5)
                execute_script()
                sleep(1)
                src_skill = src_code()
                source_skill.append(src_skill)
                            
                
                implicitly_wait(10) #implicit wait for 10 seconds   
                gotourl('{}'.format(selected_list[i] + 'details/experience/' ))
                sleep(2.5)
                execute_script()
                sleep(1)
                src_exp = src_code()
                source_experience.append(src_exp)

            close()


            name_list = []
            current_position_list = []
            current_location_list = []
            person_skills_list = []
            person_experience = []
            li_list = []
            main = []
            for i in range(0,len(source_main)):
                soup_main = BeautifulSoup(source_main[i])
                name_div = soup_main.find('div',{'class':'mt2 relative'})
                name = name_div.find('h1',{'class':'text-heading-xlarge inline t-24 v-align-middle break-words'}).get_text().strip()
                name_list.append(name)
                position = name_div.find('div',{'class':'text-body-medium break-words'}).get_text().strip()
                current_position_list.append(position)
                location = name_div.find('span',{'class':"text-body-small inline t-black--light break-words"}).get_text().strip()
                current_location_list.append(location)
                
                soup_skill = BeautifulSoup(source_skill[i])
                skill_div = soup_skill.find_all('span',{'class':'mr1 t-bold'})
                skills = []
                for j in range(0,len(skill_div)):
                    skill = skill_div[j].find('span').text
                    skills.append(skill)
                person_skills_list.append(list(set(skills)))

                soup_exp = BeautifulSoup(source_experience[i])
                section = soup_exp.find('section',{'class':'artdeco-card ember-view pb3'})
                span_len = section.find_all('span',{'aria-hidden':'true'})
                liss = []
                for j in range(0,len(span_len)):
                    split_a_1 = """<span aria-hidden="true"><!-- -->"""
                    split_a_2 = """<span aria-hidden="true"><br/><!-- -->"""
                    split_a_3 = """<span aria-hidden="true"><span class="white-space-pre"> </span>"""
                    split_a_4 = """<span aria-hidden="true"><strong><!-- -->"""
                    split_a_5 = """<span aria-hidden="true"><li-icon aria-hidden="true" class="v-align-text-bottom" size="small" type="linkedin-inbug-color-icon">"""
                    split_b = """<!-- --></span>"""
                    if str(span_len[j]).split(split_a_1)[0] == '':
                        fi_split = str(span_len[j]).split(split_a_1)
                    elif str(span_len[j])[0:63] == split_a_3:
                        fi_split = str(span_len[j]).split(split_a_3)
                    elif str(span_len[j])[0:41] == split_a_4:
                        fi_split = str(span_len[j]).split(split_a_4)
                    elif str(span_len[j])[0:127] == split_a_5:
                        fi_split = str(span_len[j]).split(split_a_5)
                    else:
                        fi_split = str(span_len[j]).split(split_a_2) 
                    if '<br/>' not in fi_split[1]:
                        se_split = str(fi_split[1]).rsplit(split_b)
                    liss.append(se_split[0])
                person_experience.append(liss)
                
                soup_exp = BeautifulSoup(source_experience[i])
                section = soup_exp.find('section',{'class':'artdeco-card ember-view pb3'})
                span_len = section.find_all('span',{'class':'t-14 t-normal t-black--light'})
                lii_list = []
                for j in range(0,len(span_len)):
                    split_a_1 = """<span aria-hidden="true"><!-- -->"""
                    split_b = """<!-- --></span>"""
                    fi_split = str(span_len[j]).split(split_a_1)
                    se_split = str(fi_split[1]).rsplit(split_b)
                    if '·' in se_split[0]:
                        new_split = str(se_split[0]).split('·')
                    lii_list.append(new_split[0])
                li_list.append(list(set(lii_list)))  
                temp = []
                for j in range(0,len(li_list[i])):
                    split_test = li_list[i][j].split('- ')
                    temp.append(split_test)
                main.append(temp)
                
            currentDate = datetime.date.today()
            currentMonthName = calendar.month_name[currentDate.month]

            z = str(currentMonthName[0:3]) +' '+ str(currentDate.year) + ' '

            for i in range(0,len(main)):
                for j in range(0,len(main[i])):
                    if main[i][j][1] == 'Present ':
                        main[i][j][1] = z
                        
            exp_count = []
            for i in range(0,len(main)):
                nil = 0
                for j in range(0,len(main[i])):
                    val = relativedelta(parser.parse(main[i][j][1]),parser.parse(main[i][j][0])).years + (relativedelta(parser.parse(main[i][j][1]),parser.parse(main[i][j][0])).months+1)/12
                    nil = nil + val
                total = nil*12
                yrs = int(total/12) 
                mon = int(total % 12)
                if mon < 10:
                    mon = "{0:0=2d}".format(mon) 
                output = str(yrs)+'.'+str(mon)
                exp_count.append(float(output))
           
            data = {'Link':selected_list,
                    'Name':name_list,
                    'Current_Position':current_position_list,
                    'Current_Location':current_location_list,
                    'Person_Skill':person_skills_list,
                    'Person_Experience':exp_count
                }

            df = pd.DataFrame(data)
            st.dataframe(data=df)
            st.markdown(get_table_download_link(df), unsafe_allow_html=True)





