

# In[1]:

import pandas as pd
from geopy.geocoders import GoogleV3
geolocator = GoogleV3(api_key = "AIzaSyDm7eUv9b0F-7vKsD8xIXR4YL500nw8Lms", timeout=1)

import io
import sys 


# In[2]:

sys.getdefaultencoding()


# In[16]:

# sys encoding from ascii to utf-8
reload(sys)  
sys.setdefaultencoding('utf8')

# In[4]:
# csv file with country names, 2 and 3 letter acronyms
# the file will help link all the documents
country_code = pd.read_csv('country_abb.csv')
#country_code = country_code['A'].str.replace('')
country_code.head()


# In[5]:
# this file has the addresses from which we want coordinates
df_sites = pd.read_excel('locataions_list.xlsx',header=5)
df_sites.head()

# In[6]:
# general location-name clean-up
df_sites = df_sites.rename(index=str, columns={'Building Country':'ALPHA-3 Code','Building City':'City','Building Address 1':'Address'})
df_sites['ALPHA-3 Code'] = df_sites['ALPHA-3 Code'].str.replace('TR','TUR') # have to replace Turkey alpha-3 key
# there is no South Melbourne, replace to Melbourne
df_sites['City'] = df_sites.City.str.replace('SOUTH ','')
df_sites.head()


# In[7]:

# merge datasets on ALPA-3 column
prop1 = pd.merge(df_sites,country_code,how='left',on='ALPHA-3 Code')
prop1.head()


# In[8]:

#prop1 = prop1.drop(['Unnamed: 23', 'Unnamed: 24'], axis=1)
# count number of NA rows in each column
prop1.isnull().sum()


# In[9]:

prop1[prop1.Country.isnull()]


# In[10]:

country_code[country_code['ALPHA-2 Code'] == 'TR']
#country_code[country_code['ALPHA-3 Code'] == 'UK']


# In[ ]:




# In[11]:

prop1["add_city_country"] = prop1["Address"] + ", " + prop1['City'] + ", " +prop1["Country"]


# In[12]:

prop1["add_city_country"].head()


# # Hit the Google Maps API to retrieve Latitude, Longitude, Address
# 
# ### encoding for international language will cause some results to be 0
# 
# #### https://stackoverflow.com/questions/21129020/how-to-fix-unicodedecodeerror-ascii-codec-cant-decode-byte
# 
# #### https://nedbatchelder.com/text/unipain.html

# In[17]:

# CREATE A LOOP THAT WILL USE THE DATAFRAME COLUMN 'ADD_CITY_COUNTRY', QUERY AND MATCH GOOGLE MAPS API, 
#	RETURN LAT AND LONG COORDINATES AND GOOGLE MAPS ADDRESS WHICH CAN HOPEFULLY BE USED AS A KEY

lat = []
lon = []
address_api = []

for i in prop1.add_city_country:
    print i
    x = geolocator.geocode(i, timeout=5, language='en')
    try:
        if x.latitude is not None:
            lat.append(x.latitude)
            lon.append(x.longitude)
            address_api.append((x.address).decode('utf8', 'ignore'))
            #print(lat, lon, address)
            print('Success')
        else:
            print('None')
            lat.append('NA')
            lon.append('NA')
            address_api.append('NA')
    except AttributeError:
        print('error')
        lat.append('NA')
        lon.append('NA')
        address_api.append('NA')


# In[18]:
# check that all lists are same size so they can be appended back to the dataframe
len(lon), len(lat), len(address_api), len(prop1)


# In[19]:

type(lon[1]), type(lat[1]), type(address_api[11])


# In[21]:

prop1['Latitude'] = lat
prop1['Longitude'] = lon
prop1['Address_api'] = address_api

prop1[['Address', "Address_api"]].head(11)


# In[22]:

prop1.to_excel('New_df_sitesList.xlsx', encoding='utf8')


# In[ ]:



