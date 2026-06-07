import streamlit as st

<<<<<<< HEAD
st.title("🧮  My Web Calculator")
=======
st.title("🧮 ကျွန်ုပ်၏ Web Calculator")
>>>>>>> c6e796683eed3f81c783ffaee4649685ee0dfd32

num1 = st.number_input("ပထမဂဏန်း ရိုက်ထည့်ပါ", value=0.0)
num2 = st.number_input("ဒုတိယဂဏန်း ရိုက်ထည့်ပါ", value=0.0)

operation = st.selectbox("တွက်ချက်မည့် ပုံစံကို ရွေးပါ", ["ပေါင်းရန် (+)", "နုတ်ရန် (-)", "မြှောက်ရန် (*)", "စားရန် (/)"])

if st.button("တွက်ချက်မည်"):
    if operation == "ပေါင်းရန် (+)":
        result = num1 + num2
    elif operation == "နုတ်ရန် (-)":
        result = num1 - num2
    elif operation == "မြှောက်ရန် (*)":
        result = num1 * num2
    elif operation == "စားရန် (/)":
        if num2 != 0:
            result = num1 / num2
        else:
            result = "Error (သုညဖြင့် စား၍မရပါ)"
            
<<<<<<< HEAD
    st.success(f"ရလဒ်မှာ = {result}")
    st.markdown("------")
    st.write("Developed by AKKW")
=======
    st.success(f"ရလဒ်မှာ = {result}")
>>>>>>> c6e796683eed3f81c783ffaee4649685ee0dfd32
