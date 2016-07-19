from bs4 import BeautifulSoup
from pandas import Series, DataFrame
import lxml
import pandas as pd

def addon(working_dict,name,aspect):
    value=aspect
    if value==None:
        working_dict[name].append(value)
    else:
        working_dict[name].append(value.get_text())


def create_explore(filename):
    country=BeautifulSoup(open(filename),'xml')
    revisions=country.find_all("revision")   

    country_dict={'Category':[],'timestamp':[],'username':[]}

    for edit in revisions:
        addon(country_dict,'Category',edit.parent.title)
        addon(country_dict,'timestamp',edit.timestamp)
        addon(country_dict,'username',edit.username)

    dates=pd.to_datetime(country_dict['timestamp']).to_period('M')

    cf=DataFrame(country_dict,index=dates)

    return(cf)

def get_series(dataframe,category_index):
    cat=unique(dataframe.Category)[category_index]
    country_cat=dataframe[dataframe.Category==cat]
    country_time_idx=country_cat.groupby(country_cat.index).count()
    country_time_cat=country_time_idx.Category
    return(country_time_cat)



def makeplots(dataframe,category_index, title):
    country_cat=dataframe[dataframe.Category==unique(dataframe.Category)[category_index]]
    country_time_idx=country_cat.groupby(country_cat.index).count()
    country_time_idx.plot(legend=None,title=title)
   

thailand=create_explore("Wikipedia-20160718223915.xml")

iran=create_explore("Wikipedia-20160718222006.xml")

turkey=create_explore("Wikipedia-20160718000517.xml")

tur_mil=get_series(turkey,8)
iran_mil=get_series(iran,16)
thai_mil=get_series(thailand,8)

index=pd.period_range('1-2006','8-2016',freq='M')

tur_econ=get_series(turkey,2)
iran_econ=get_series(iran,4)
thai_econ=get_series(thailand,2)

econ_frame=DataFrame(index=index)
econ_frame['Turkey']=tur_econ
econ_frame['Iran']=iran_econ
econ_frame['Thailand']=thai_econ
econ_frame.plot(kind='bar', title='Economy Edits')

##There seem to be more edits in the year before an event than usual. These may also line up with elections; this is just a quick eyeball.