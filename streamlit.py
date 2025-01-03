import streamlit as st
from financial_agents import Myagent

agent=Myagent()

st.title("Chat Interface")

user_input=st.text_input("Enter financial Enquiry about a company")

if st.button("search"):
    if user_input:
        result=agent.process_agents(user_input)
        print(result)
        st.write(f"Results are:{result}")
    else:
        st.write("Kindly give a query")


