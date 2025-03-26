
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import random 
import pandas as pd
import statistics

def csv_to_json():
    """
    from src csv, build json 
    """

    print("hello!")

    fil = "samples"
    fil = "samples03"
    src_fol = os.path.join("baking", "src")
    src_fil = os.path.join(src_fol, "Mycobaking - " + fil + ".csv")
    df = pd.read_csv(src_fil)
    print(src_fil)

    print(df)

    col_names = df.columns
    print(col_names)

    for col_name in col_names: 

        print(col_name)

        unique = unique_list(df, col_name)
        print(unique)


    dst_json = {}
    dst_json = add_json_list(df, "strain substrate")

    
    dst_fol = os.path.join("code", "json")
    dst_fil = os.path.join(dst_fol, "mycobake.json")
    save_json(dst_fil, dst_json)

    list_for_boxplot(dst_json, fil)



def list_for_boxplot(dst_json, fil):
    """
    list for boxplot
    """

    for key in dst_json:
        
        print("key = ") 
        print(key)

        drybywets = []
        names = []

        for i in range(len(dst_json[key])):

            name = str(dst_json[key][i]["name"])
            print(type(name))

            print("name found = " + name)

            x = dst_json[key][i]["dry by wet"]
            names.append(dst_json[key][i]["name"])
            drybywets.append(x)

    #print(drybywets)
    #print(names)

 
    plt.figure(figsize=(11, 5))

    
    

    box = plt.boxplot(drybywets, vert=False, patch_artist=True, medianprops=dict(color='black', linewidth=2), widths=0.95)

    # Define different colors for each box
    gano_luc = [0.68, 0.85, 0.9, 0.5]
    gano_spp = [0.87, 0.63, 0.87, 0.5]
    pleu_ost = [1.0, 0.5, 0.0, 0.5]
    colors_face = [gano_spp, pleu_ost, gano_luc, pleu_ost, gano_spp, gano_luc, pleu_ost, gano_spp, gano_luc]


   # Define different colors for each box
    gano_luc = [0.476, 0.595, 0.63]
    gano_spp = [0.609, 0.441, 0.609]
    pleu_ost = [0.7, .35, 0.0]
    colors_edge = [gano_spp, pleu_ost, gano_luc, pleu_ost, gano_spp, gano_luc, pleu_ost, gano_spp, gano_luc]
    colors_whisker = [gano_spp, gano_spp, pleu_ost, pleu_ost, gano_luc, gano_luc, pleu_ost, pleu_ost, gano_spp, gano_spp, gano_luc,gano_luc,  pleu_ost, pleu_ost, gano_spp, gano_spp, gano_luc, gano_luc]


    # Apply colors to each box
    for patch, color in zip(box['boxes'], colors_face):
        patch.set_facecolor(color)

    # Apply colors to each box
    for patch, color in zip(box['boxes'], colors_edge):
        patch.set_edgecolor(color)


    for whisker, color in zip(box['whiskers'], colors_whisker):
        whisker.set_color(color)
        whisker.set_linewidth(2)

    # Apply different colors to caps
    for cap, color in zip(box['caps'], colors_whisker):
        cap.set_color(color)
        cap.set_linewidth(2)
    




    plt.xlabel("Dry Matter Ratio (Dry / Wet Weight)  " + "\n" + "majority of wet weight lost during baking <--> majority of wet weight remains after baking")
    #plt.ylabel("Strain, Substrate")
    plt.yticks(range(1, len(names) + 1), names)
    plt.subplots_adjust(left=0.35)
    plt.xlim(0, 1)  # Limits from 0 to 1
    plt.grid(axis='x', linestyle='--', color='gray', linewidth=0.7)

    add_scatter(dst_json)
    
    plot_dst = os.path.join("baking", fil + ".png")
    plt.savefig(plot_dst, dpi=300, bbox_inches="tight")  # Save as PNG
    plt.show()
    

def add_scatter(dst_json):
    """
    add scatter 
    """


    for key in dst_json:
        
        print("key = ") 
        print(key)

        drybywets = []
        names = []

        for i in range(len(dst_json[key])):

            name = str(dst_json[key][i]["name"])
            print(type(name))

            print("name found = " + name)

            xx = dst_json[key][i]["dry by wet"]
            
            
            yy = []
            for x in xx: 

                fac = 0.7

                if x > np.median(xx): fac = (max(xx) - x)/(max(xx) - np.median(xx))*fac 
                elif x < np.median(xx): fac = (x - min(xx))/(np.median(xx) - min(xx))*fac 


                ran = fac*random.random()
                yy.append(i+1-fac/2+ran)

            plt.scatter(xx,yy, color=[0.6, 0.6, 0.6], edgecolors = [0.3, 0.3, 0.3], linewidths=.2, s=12)

    
    


def add_json_list(df, col_name):
    """
    return json
    """

    dst_json = {}
    unique = unique_list(df, col_name)
    print(unique)

    temps = []
    for uni in unique: 

        temp = {"name": uni}

        cols_of_interest = ["wet weight", "dry weight"]

        for col_of_interest in cols_of_interest:

            values = list_variables(df[df[col_name] == uni], col_of_interest)

            temp[col_of_interest] = values
            temp["len"] = len(values)

        
        temp["dry by wet"] = dry_by_wet(temp)
        temp["avg"] = sum(list(temp["dry by wet"]))/len(list(temp["dry by wet"]))
        temp["max"] = max(list(temp["dry by wet"]))
        temp["min"] = min(list(temp["dry by wet"]))
        temp["stdev"] = np.std(list(temp["dry by wet"]), ddof=1)
        temp["median"] = np.median(list(temp["dry by wet"]))
        temp["mean"] = np.mean(list(temp["dry by wet"]))

        temp["quan25"] = np.quantile(list(temp["dry by wet"]), 0.25)
        temp["quan75"] = np.quantile(list(temp["dry by wet"]), 0.75)

        temp["var"] = np.var(list(temp["dry by wet"]))
        temp["cv"] = np.std(list(temp["dry by wet"])) / np.mean(list(temp["dry by wet"]))



        temp["range"] = temp["max"] - temp["min"]

        temps.append(temp)

        sorted_list = sorted(temps, key=lambda x: x["avg"], reverse=False)


    dst_json = {"strain substrate": sorted_list}

    return dst_json


def dry_by_wet(temp):
    """
    return list
    """

    dry = temp["dry weight"]
    wet = temp["wet weight"]

    values = []
    for i in range(len(dry)):

        value = dry[i]/wet[i]
        values.append(value)
    
    return(values)





def list_variables(df, col_name):
    """
    
    """

    values = list(df[col_name])
    return(values)








def save_json(dst_fil, data):
    """
    save json
    """

    with open(dst_fil, "w") as json_file:
        json.dump(data, json_file, indent=4)  # indent=4 makes it human-readable





def unique_list(df, name):
    """
    return list of unique values
    """

    unique = []
    for i in range(len(list(df[name]))):

        value = list(df[name])[i]
        if value in unique: continue 
        unique.append(value)
        #unique.sort

    #print(unique)
    return(unique)





def main():
    """
    """

    print("running main")

    tasks = [0, 1]

    # build json 
    if 0 in tasks: csv_to_json()



    print("completed main")


if __name__ == "__main__":
    main()



