import streamlit as st

col1,buff, col2 =st.columns([2,.3,2])
with col1:
    st.subheader("Expander example")

    st.write("""Doing stuff on every page load

...

Finished doing stuff""")

    with st.expander("Do you want to see more?"):
        st.write("Doing more optional stuff")

with col2:
    if "more_stuff" not in st.session_state:
        st.session_state.more_stuff = False

    st.subheader("Button example")

    st.write("""Doing stuff on every page load

...

Finished doing stuff""")


    click = st.button("Do you want to see more?")
    if click:
        st.session_state.more_stuff = True

    if st.session_state.more_stuff:
        st.write("Doing more optional stuff")