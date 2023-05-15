import streamlit as st

class Counter:
    def __init__(self):
        if 'count' not in st.session_state:
            st.session_state.count = 0
        if 'title' not in st.session_state:
            st.session_state.title = "Calculator"
        self.col1, self.col2 = st.columns(2)

    def add(self):
        st.session_state.count += 1

    def subtract(self):
        st.session_state.count -= 1

    def tester(self):
        if 'tester' not in st.session_state:
            st.session_state.tester = "Tester"
        else:
            st.session_state.tester = "Already tested"
        with self.col2:
            st.write(f"Hello from the {st.session_state.tester}!")

    def window(self):

        with self.col1:
            st.button("Increment", on_click=self.add)
            st.button("Subtract", on_click=self.subtract)
            st.write(f'Count = {st.session_state.count}')
        with self.col2:
            st.button('test me', on_click=self.tester)



if __name__ == '__main__':
    ct = Counter()
    ct.window()