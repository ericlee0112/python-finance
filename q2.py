#constants
price_of_streetcar = 6000000
annual_cost = 25000
#operating costs increase by 10 percent every year
multiplier = 1.1
#streetcars can be sold to egypt at lump price of 3000000
#this price depreciates by 5% every year
#next year price = 0.95*(this year price)

#life_span = 35 years
#after 35 years, sold for 10000/streetcar

#determine whether the TTC should keep the current streetcar for an additional year
#or purchase a brand new streetcar and get rid of the old one (either sell it to Alexandria or for 

dict = {}
dict[0] =  max(6000000,-3000000)
for t in range(1,36):
    costOfKeeping = (25000*(1.1)**t)*(0.95**t)
    valueSell = (3000000*(0.95)**t)*(0.95**t)
    if costOfKeeping > valueSell:
        dict[t] = "keep : " + str(valueKeep)
    else:
        dict[t] = "sell : " + str(valueSell)

for key in dict:
    print("year " + str(key) + " : " + str(dict[key]))