#tracker streamlit app
import streamlit as st
import pandas as pd
import numpy as np
import gspread_pandas as gp
import datetime


###############################################################################################
####################################### STREAMLIT UI ##########################################
###############################################################################################

st.set_page_config(page_title = 'Simple CRUD', layout = 'wide')

cols = st.columns(3)
cols[1].write('# Simple CRUD')

#select mode
modus = st.sidebar.selectbox('Select mode: ', ['none', 'display standards','add new formula version', 'search db'])

##############################################################################################
######################################### AUTHORIZE ##########################################
##############################################################################################

def get_gspread_creds():
    gspread_config = gp.conf.get_config(conf_dir = './', file_name = 'api_access.json')
    gspread_creds = gp.conf.get_creds(config = gspread_config, save = True, creds_dir = './', user = 'api_access_creds_gspread.txt')
    return gspread_creds

gspread_creds = get_gspread_creds()

##############################################################################################
######################################## LOAD GSHEET DB ######################################
##############################################################################################

#replace with URL of Google sheet
sheet_url='path-to-database'
spread = gp.Spread(sheet_url, creds = gspread_creds)      
df = spread.sheet_to_df(index = 0)

# drop any null value columns to avoid errors
df.dropna(inplace = True)

#cast as many cols as you can to numeric
df = df.apply(pd.to_numeric, errors='ignore')

if modus == 'none':
    st.write('Select database function')

##############################################################################################
################################### DISPLAY STANDARD MEDIA ###################################
##############################################################################################

#standards indicated by 'y' in standard column
elif modus == 'display standards':
    #filter input df by standard col
    stds = df[df['standard']=='y']
    stds['name'] = stds['formula name'].astype(str) + 'v' + stds['version'].astype(str)
    st.write('Current operation versions: ')
    st.write(stds['name'])

##############################################################################################
################################### ADD NEW MEDIUM VERSION ###################################
##############################################################################################
elif modus == 'add new formula version':
    new_formula=[]

    df['ID']=df['ID'].astype(str)
    #get id list and make new number
    latest = list(df['ID'])[-1].lstrip('0')
    newest = int(latest) + 1
    new_fmt = "{num:05d}".format(num=newest)
    st.write("ID : ", new_fmt)

    #start off our output df with the new ID number
    new_formula.append(new_fmt)

###########populate from pre-defined ingredients list? would need to allow user option to leave blank
    #input form
    with st.form(key='media_db_cols'):
        cols = st.columns(6)
        values = {}
        for i,col in enumerate(cols):
            colname= df.columns.values[i+1]
            values[i] = col.text_input(f'Input for {df.columns.values[i+1]}', key=str(i))

        user=st.text_input(label='creator')
        notes=st.text_input(label='notes')
        standard_in = st.radio('Standard?',['n','y'])

        for el in values.keys():
            new_formula.append(values[el])
            
        new_formula.append(user)
        new_formula.append(notes)
        new_formula.append(str(datetime.datetime.now()))
        if standard_in == 'y':
            new_formula.append('y')

        else:
            new_formula.append('n')

        subt = st.form_submit_button("Add new formula")
        if subt:
            st.success('New formula submitted!')
            st.write(new_formula)
            st.write(len(new_formula))

            #get first empty row in df
            newrow = len(df) + 1
            len(new_formula)
            c=len(df.columns) - 1
            spread=spread.update_cells((newrow,1),(newrow,c),new_formula)

##############################################################################################
###################################### QUERY FUNC ############################################
##############################################################################################

elif modus == 'search db':

    search = st.sidebar.expander('Search bar')
    st.sidebar.write('Enter search terms separated by comma. Returns rows w/ at least a partial match for all terms. Order/case don\'t matter.')
    s_in = search.text_input('search string')

    s_b = search.button('Search media database')

    def search_fun(s,df):
        #split up string by commas
        slist = s.split(",")
        #subset df for each list 
        frameList=[]
        for el in slist:
            subs_df = df[df.apply(lambda r: r.str.contains(el).any(), axis=1)] 
            frameList.append(subs_df)

        df_merge = frameList[0]
        for df in frameList[1:]:        
            df_merge = pd.merge(df_merge, df, how='inner')

        return df_merge

    if s_b:
        out = search_fun(s_in,df)
        if len(out)>0:
            st.write('Search results')
            st.write(out)#display dataframe results

    #will never display as long as at least the 1st search term returns results
        elif len(out)==0:
            st.warning('No results found. Try different search string')

