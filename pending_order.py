# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col,when_matched

st.title(":cup_with_straw: Pending Smoothie Orders :cup_with_straw:")
st.write(
    """Orders that need to filled
    """
)
cnx=st.connection("snowflake")
session=cnx.session()  
#session = get_active_session()
my_dataframe = session.table("smoothies.public.orders").filter(col('ORDER_FILLED')==0).collect()
#st.dataframe(data=my_dataframe, use_container_width=True)

if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    
    time_to_insert=st.button('Submit Order');
    if time_to_insert:
        try:
            og_dataset = session.table("smoothies.public.orders")
            edited_dataset = session.create_dataframe(editable_df)
            og_dataset.merge(edited_dataset
                             , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                             , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                            )
            st.success('Your Smoothie is ordered!', icon="👍")
        except:
            st.write('Something went wrong');
    
else:
    st.success('There are no pending orders right now', icon="👍")
