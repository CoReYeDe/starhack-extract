import streamlit as st
import requests

def fetch(session, url):
    try:
        result = session.get(url)
        return result.json()
    except Exception:
        return {}


def main():
    
    session = requests.Session()
        
    st.set_page_config(page_title="Starhack Waste Watchers", page_icon="🤖")
    st.title("Hello Waste Watchers")
    st.header("Init-WebApp")
    request_title = 'Request'
    response_title = 'Response'

    st.write(f'This is a {request_title}')

    st.json({
        "id": "1655801622",
        "userId": 1337,
        "mhd": "23-06-2022",
        "marketCode": 21,
        "articleNumber": 10
    })

    st.write(f'This is a {response_title}')

    st.json({
       "id": "1655801622",
       "dbId": "DBID",
       "userId": "1337",
       "mhd": "23-06-2022",
       "days": "2",
       "paybackpoints": "6",
       "productName": "Hack-Kekse"
    })

    with st.form("my_form"):
        index = st.number_input("ID", min_value=0, max_value=100, key="index")

        submitted = st.form_submit_button("Submit")

        if submitted:
            st.write("Result")
            data = fetch(session, f"https://picsum.photos/id/{index}/info")
            if data:
                st.image(data['download_url'], caption=f"Author: {data['author']}")
            else:
                st.error("Error")


if __name__ == '__main__':
    main()