from selenium import webdriver  
import time
from webdriver_manager.chrome import ChromeDriverManager
import streamlit as st
from diver import * 
   
st.sidebar.success("LINKEDIN RECURITER OPTION")


def app():
    st.title('LINKEDIN RECURITER LOGIN ')


    with st.form("my_form"):

        userid_1 = st.text_input('Enter Linkedin username/mail :')
        pass_word_1 = st.text_input('Enter Linkedin password :',type="password")
        userid_2 = st.text_input('Enter Microsoft office username/mail :')
        pass_word_2 = st.text_input('Enter Microsoft office password :',type="password")


        submitted_new = st.form_submit_button("LOGIN")
        if submitted_new:
            diver()
            gotourl("https://www.linkedin.com/talent/home")    
            sleep(3)
            find_element_xpath_click_send_keys("""//*[@id="username"]""",userid_1) #EMAIL ONE
            find_element_xpath_click_send_keys("""//*[@id="password"]""",pass_word_1) #PASSWORD
            find_element_xpath_click("""//*[@id="app__container"]/main/div[2]/form/div[3]/button""") #SUBMIT 
            sleep(3)
            ### ENTER 
            find_element_xpath_click("""/html[1]/body[1]/div[4]/div[5]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[1]/ul[1]/li[1]/div[1]/div[2]/button[1]""") # ENTER CORPORATE ACCOUNT

            sleep(5)

            ### company login office

            find_element_xpath_click_send_keys("""/html[1]/body[1]/div[1]/form[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/input[1]""",userid_2) # COMPANY USER ID
            sleep(3)
            find_element_xpath_click("""/html[1]/body[1]/div[1]/form[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[1]/input[1]""")
            sleep(3)
            find_element_xpath_click_send_keys("""/html[1]/body[1]/div[1]/form[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]/input[1]""",pass_word_2) # COMPANY PASSWORD
            sleep(3)
            find_element_xpath_click("""/html[1]/body[1]/div[1]/form[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[2]/div[1]/div[4]/div[2]/div[1]/div[1]/div[1]/div[1]/input[1]""") #SUBMIT
            sleep(3)

            ### user perfrorms actions for next 100 sec (select authentication mode and verify it)
            

