import random 

def weekly_meal(lst1, lst2, lst3, lst4):
    """
    lst1 : carbohydrate menu list
    lst2 : soup menu list
    lst3 : main menu list
    lst4 : sub menu list *allow repetition
    """
    weekly = {}
    
    l1 = random.sample(lst1, 10)
    l2 = random.sample(lst2, 10)
    l3 = random.sample(lst3, 10)
    l4 = random.choices(lst4, 10)

    for i in range(0, 10-1,2):
        #0,1 / 2,3 / 4,5 / 6,7 / 8,9
        l=[]
        #lunch
        l.append(lst1[i]) 
        l.append(lst2[i])
        l.append(lst3[i])
        l.append(lst4[i])
        #dinner
        l.append(lst1[i+1]) 
        l.append(lst2[i+1])
        l.append(lst3[i+1])
        l.append(lst4[i+1])
        weekly[i] = l
    
    print(weekly)

def comparision_of_modes():
    pass   

    #model_lst : names of model
    #model 
    #train/test
    #score
    #score_lst
    #best model


def amount_per_person() :
    pass
    #weekly[""]


def amount_total_person() :
    pass



    
        