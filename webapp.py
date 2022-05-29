# imports
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', 40)
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
sns.set_style('darkgrid')
import plotly.express as px
import streamlit as st
import warnings
warnings.filterwarnings('ignore');

#loading dataset into a dataframe
df = pd.read_csv('Data//cars_ds_final_2021.csv')

#Checking ad exploring data set
desc= df.describe()
grp =df.groupby("Model")[["Variant" , "Ex-Showroom_Price"]].count()
#print(des,grp)

#cleaning up data
df['car'] = df.Make + ' ' + df.Model
c = ['Make','Model','car','Variant','Body_Type','Fuel_Type','Fuel_System','Type','Drivetrain','Ex-Showroom_Price','Displacement','Cylinders',
     'ARAI_Certified_Mileage','Power','Torque','Fuel_Tank_Capacity','Height','Length','Width','Doors','Seating_Capacity','Wheelbase','Number_of_Airbags']
df_full = df.copy()
df['Ex-Showroom_Price'] = df['Ex-Showroom_Price'].str.replace('Rs. ','',regex=False)
df['Ex-Showroom_Price'] = df['Ex-Showroom_Price'].str.replace(',','',regex=False)
df['Ex-Showroom_Price'] = df['Ex-Showroom_Price'].astype(int)
df = df[c]
df = df[~df.ARAI_Certified_Mileage.isnull()]
df = df[~df.Make.isnull()]
df = df[~df.Width.isnull()]
df = df[~df.Cylinders.isnull()]
df = df[~df.Wheelbase.isnull()]
df = df[~df['Fuel_Tank_Capacity'].isnull()]
df = df[~df['Seating_Capacity'].isnull()]
df = df[~df['Torque'].isnull()]
df['Height'] = df['Height'].str.replace(' mm','',regex=False).astype(float)
df['Length'] = df['Length'].str.replace(' mm','',regex=False).astype(float)
df['Width'] = df['Width'].str.replace(' mm','',regex=False).astype(float)
df['Wheelbase'] = df['Wheelbase'].str.replace(' mm','',regex=False).astype(float)
df['Fuel_Tank_Capacity'] = df['Fuel_Tank_Capacity'].str.replace(' litres','',regex=False).astype(float)
df['Displacement'] = df['Displacement'].str.replace(' cc','',regex=False)
df.loc[df.ARAI_Certified_Mileage == '9.8-10.0 km/litre','ARAI_Certified_Mileage'] = '10'
df.loc[df.ARAI_Certified_Mileage == '10kmpl km/litre','ARAI_Certified_Mileage'] = '10'
df['ARAI_Certified_Mileage'] = df['ARAI_Certified_Mileage'].str.replace(' km/litre','',regex=False).astype(float)
df.Number_of_Airbags.fillna(0,inplace= True)
df['price'] = df['Ex-Showroom_Price'] * 0.014
df.drop(columns='Ex-Showroom_Price', inplace= True)
df.price = df.price.astype(int)
HP = df.Power.str.extract(r'(\d{1,4}).*').astype(int) * 0.98632
HP = HP.apply(lambda x: round(x,2))
TQ = df.Torque.str.extract(r'(\d{1,4}).*').astype(int)
TQ = TQ.apply(lambda x: round(x,2))
df.Torque = TQ
df.Power = HP
df.Doors = df.Doors.astype(int)
df.Seating_Capacity = df.Seating_Capacity.astype(int)
df.Number_of_Airbags = df.Number_of_Airbags.astype(int)
df.Displacement = df.Displacement.astype(int)
df.Cylinders = df.Cylinders.astype(int)
df.columns = ['make', 'model','car', 'variant', 'body_type', 'fuel_type', 'fuel_system','type', 'drivetrain', 'displacement', 'cylinders',
              'mileage', 'power', 'torque', 'fuel_tank','height', 'length', 'width', 'doors', 'seats', 'wheelbase','airbags', 'price']


#Working with streamlit and customising the webpage
st.set_option('deprecation.showPyplotGlobalUse', False)

#Heading
st.markdown("<h1 style='text-align: center; color:#bde0fe;'>AUTOMOB - ALLY</h1>", unsafe_allow_html=True)
st.image('Data//Automob_GIF.gif',"Your instant Automobile Ally is here!!",750)

#Navigation bar   
st.sidebar.image('Data//AUTOMOB-ALLY.png')
st.sidebar.header("NAVIGATION BAR")
#defining the nav bar tabs
rad = st.sidebar.radio(" ", [ "Home", "Analysis By Body and Fuel Type", "Correlation Matrix",
                              "Interactive Plot : Power Vs Price Vs Mileage","Competitor Analysis", "Price Analysis"])



#Calculators to calculate the actual values that were scaled down
def PriceCalc():
    st.write(" PRICE CALCULATOR")
    st.write('''Actual Market price of the vehicle is 'Price(shown in the table) divided by 0.014
             (Which was taken for easy scaling of graphs). Here is a calculator for calculating the market price:''')
    p = st.number_input("Type your price here", 3310)
    PRICE = p/0.014
    st.write(PRICE)

def PriceScaler():
    st.write(" PRICE SCALER")
    st.write('''Actual Market price of the vehicle is 'Price(shown in the table) divided by 0'
             (Which was taken for easy scaling of graphs). Here is a calculator for calculating the price to select on the slider bar below:''')
    p = st.number_input("Type your desired price here", 236429)
    PRICE = p*0.014
    st.write(PRICE)

def PowerCalc():
    st.write(" POWER CALCULATOR")
    st.write('''Actual Horsepower of the vehicle is 'Power (shown in the table) divided by 0.98632
             (Which was taken for easy scaling of graphs). Here is a calculator for calculating the actual power:''')
    p = st.number_input("Type your price here", 33.53)
    POWER= p/0.98632
    st.write(POWER)

def rmse(target,prediction):
    return np.sqrt(((prediction - target) ** 2).mean())

  


#Home_Page
if rad == "Home" :
    st.subheader('''Welcome!! Greeting dear user!''')
    st.write('''Being a automobile manufacturer is no longer a thing of difficulty with your very own 'interactive' web ally, Automob-Ally.
                Let's begin by looking at the state of the automobile industry to evaluate its condition using this data.
            ''')
    st.write('The current statistics about Automobile has been displayed here. This data frame has been used for further Analysis in the other tabs')
    #displaying dataframe
    st.dataframe(df,4000,1000)
    #footer
    st.write(" ")
    st.write(" ")
    #description
    desc = df.describe()
    st.write("Here is a vivid description of the data:")
    st.dataframe(desc)
    st.write(''' Displacement is in cc, Mileage is in km/litres, power is in 1.014 hp,torque is N-m,
                 fuel tank is in litres,length, height and width are all in mm, wheelbase is also in mm and  price is in 71.42 Ruppes
             '''
            )
    st.markdown("---")
    PriceCalc()
    PowerCalc()

#EDA

#Radio_buttons    
if rad == "Analysis By Body and Fuel Type" :
    #plotting cars by body type
    st.subheader("Analysis By Body Type")
    plt.figure(figsize=(12,6))
    sns.boxplot(data=df, x='price', y='body_type', palette='viridis')
    plt.title('Box plot of Price of every body type',fontsize=18)
    plt.ylabel('')
    plt.yticks(fontsize=14)
    plt.xticks([i for i in range(0,800000,100000)],[f'{i:,}$' for i in range(0,800000,100000)],fontsize=14)
    st.pyplot();
    st.write('''Car body type strongly influences the price. While certain types such as MPVs occupy lower ranges of prices,
             Coupe,Convertible occupy a very small part of te higher price range.''') 

    
    #Checking Fuel type
    st.subheader("Analysis By Fuel Type")
    plt.figure(figsize=(11,6))
    sns.countplot(data=df, x='fuel_type',alpha=.6, color='darkblue')
    plt.title('Cars count by engine fuel type',fontsize=18)
    plt.xlabel('Fuel Type', fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.ylabel('')
    st.pyplot();
    st.write('''Most cars have the fuel type - petrol/diesel. The overall price of petrol or diesel or gas decided by the government and the availibility
            of fuel definitely affects a buyer's opinion of purchasing a vehicle.''')

if rad == "Correlation Matrix":
    st.subheader("Correlation Matrix")
    #Correlation matrix
    plt.figure(figsize=(22,8))
    sns.heatmap(df.corr(), annot=True, fmt='.2%')
    plt.title('Correlation between differet variable',fontsize=20)
    plt.xticks(fontsize=14, rotation=320)
    plt.yticks(fontsize=14)
    st.pyplot();

    st.write('''
                Price is most closely related with power, mileage, displacement and cylinders. The following is an analysis of price with different parameters
            ''')


    st.subheader("Trends in Price")
    #Features based on correlation part 1
    st.subheader("Power Vs Price")
    #plot
    plt.figure(figsize=(10,8))
    sns.scatterplot(data=df, x='power', y='price',hue='body_type',palette='viridis',alpha=.89, s=120 );
    plt.xticks(fontsize=13);
    plt.yticks(fontsize=13)
    plt.xlabel('power',fontsize=14)
    plt.ylabel('price',fontsize=14)
    plt.title('Relation between power and price',fontsize=20)
    st.pyplot();
    #conclusion
    st.write("Hatchbacks seems to be the body type with the least horsepower and price, again showing that body type is an important factor")

    #Features based on correlation part 2
    st.subheader("Mileage Vs Price")
    #plot
    plt.figure(figsize=(10,8))
    sns.scatterplot(data=df, x='mileage', y='price',hue='body_type',palette='viridis',alpha=.89, s=120 );
    plt.xticks(fontsize=13);
    plt.yticks(fontsize=13)
    plt.xlabel('mileage',fontsize=14)
    plt.ylabel('price',fontsize=14)
    plt.title('Relation between mileage and price',fontsize=20)
    st.pyplot();
    #conclusion
    st.write("This shows that mileage and price have a negative relationship. Somehow, a more pricey vehicle has worse mileage than  less pricey one")

    #Features based on correlation part 3
    st.subheader("Displacement Vs Price")
    #plot
    plt.figure(figsize=(10,8))
    sns.scatterplot(data=df, x='displacement', y='price',hue='body_type',palette='viridis',alpha=.89, s=120 );
    plt.xticks(fontsize=13);
    plt.yticks(fontsize=13)
    plt.xlabel('mileage',fontsize=14)
    plt.ylabel('price',fontsize=14)
    plt.title('Relation between displacement and price',fontsize=20)
    #conclusion
    st.pyplot();

    st.write("For more custom analysis ---> Go to Competitor Analysis tab in the Navigation Bar")


    
if rad == "Interactive Plot : Power Vs Price Vs Mileage":
    #Power, price, Mileage
    st.subheader("Power Vs Price Vs Mileage")
    st.write("Since, Power, Price and Mileage seemed to give a somewhat close relationship, here is a scatter plot to understand more:")
    fig = px.scatter_3d(df, x='power', z='price', y='mileage',color='make',width=800,height=750)
    fig.update_layout(showlegend=True)
    st.plotly_chart(fig)
    #navigation instruction
    st.write(" Navigation through graph: Use your mouse to scroll around the graph. Hover over scatter bits to see more data.Double click on one of the legend items to isolate them and view.")


#Manual plot function
def Manualplot(arg1, arg2):
    fig = px.scatter(df, 
                     x= arg1, 
                     y= arg2, 
                     animation_frame="fuel_type", 
                     animation_group="make",    
                     color="body_type", 
                     hover_name="fuel_tank", 
                     )
    fig.update_layout(plot_bgcolor="#219ebc")
    st.plotly_chart(fig);


    
if rad == "Competitor Analysis":
    st.subheader("Competitor Analysis")
    
    #taking column name input
    plotvar1 = st.selectbox ( "Select a column to compare",
                              ['type', 'drivetrain',
                               'displacement', 'cylinders','mileage', 'power',
                               'torque', 'fuel_tank','height', 'length', 'width','doors', 'seats',
                               'wheelbase','airbags', 'price'] ,
                              index =0
                              )
    
    plotvar2 = st.selectbox ( "Select another column to compare",
                              ['type', 'drivetrain', 'displacement',
                               'cylinders','mileage', 'power', 'torque', 'fuel_tank','height','length', 'width','doors', 'seats', 'wheelbase','airbags', 'price'] ,
                              index =0
                              )
    #Plotting
    Manualplot(plotvar1, plotvar2)

    #Analysing more based on body type and fuel type
    st.markdown("---")                        
    st.write("Choose the Fuel Type and Body Type of the car you wish to release to find its competitors")
    b1 = st.selectbox("Fuel Type", ["Petrol","Diesel","Hybrid","CNG+Petrol"], index = 0)
    b2 = st.selectbox("Body Type", ['Hatchback', 'MPV', 'MUV', 'SUV', 'Sedan', 'Crossover',
                                    'Crossover, SUV', 'SUV, Crossover', 'Sedan, Crossover', 'Coupe','Convertible', 'Sedan, Coupe',
                                    'Sports, Hatchback','Sports, Convertible', 'Sports', 'Coupe, Convertible'],index = 0)
    newdf = df[(df.body_type == b2) & (df.fuel_type == b1)]
    displaydf = newdf.drop (["body_type","fuel_type"],axis=1)
    st.write("Competitors in this area are:")
    st.dataframe(displaydf, 4000,500)
    st.markdown("---")
    PriceCalc()
    PowerCalc()


if rad == "Price Analysis":
    st.subheader("Price Analysis")
    #Analysing Price
    PriceScaler()
    st.markdown("---")
    st.write("Choose the Price Range of the car you wish to release to find its competitors")
    pmin = st. slider ("Minimum Price" , min_value = 3310 , max_value = 744943)
    pmax = st.slider ("Maximum Price" , min_value = 3311 , max_value = 744944)
    newdf = df[(df.price >= pmin) & (df.price <= pmax)]
    st.write("Cars in this price range are:")
    st.dataframe(newdf, 4000,1000)
    st.markdown("---")
    PriceCalc()
    PowerCalc()



