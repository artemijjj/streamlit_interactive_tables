import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
import pandas as pd


upl_file = st.sidebar.file_uploader('', type=["csv"])

cod = st.sidebar.selectbox('Выберите кодировку:', ['cp1251', 'utf8'])
delim = st.sidebar.selectbox('Выберите разделитель:', [',', ';', '|'])


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode(cod)


if upl_file is not None:
    df = pd.read_csv(upl_file, encoding=cod, delimiter=delim)
    show_df = st.sidebar.checkbox('show_data', value=True)
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=True, enablePivot=True, enableValue=True, enableRowGroup=True)
    gb.configure_selection('multiple', use_checkbox=True)
    gb.configure_side_bar()
    gridoptions = gb.build()
    if show_df:
        response = AgGrid(df, height=1000,
                          width='100%',
                          gridOptions=gridoptions,
                          enable_enterprise_modules=True,
                          update_mode=GridUpdateMode.MODEL_CHANGED,
                          data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
                          fit_columns_on_grid_load=False,
                          header_checkbox_selection_filtered_only=True,
                          use_checkbox=True)

        v = response['selected_rows']
        if v:
            st.write('Selected rows')
            st.dataframe(v)
            dfs = pd.DataFrame(v)
            csv = convert_df(dfs)

            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='selected.csv',
                mime='text/csv',
            )

# show_df = st.sidebar.checkbox('show_data')
# if show_df == True:


# df = pd.read_csv(uploaded_file)
# st.write(df)
# df = pd.read_csv
