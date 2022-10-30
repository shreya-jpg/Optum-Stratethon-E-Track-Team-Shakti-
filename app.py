import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from insurance_company import *
from nearestorgfinder import *
from scipy.stats import norm
app = Flask(__name__)

condition_desc_to_code = pickle.load(open('pickles/condition_description_to_code.pickle', 'rb'))
condition_code_to_careplan_code = pickle.load(open('pickles/condtioncode_to_listofcareplancodes.pickle', 'rb'))
careplan_code_to_careplan_desc = pickle.load(open('pickles/careplancode_to_careplandescription.pickle', 'rb'))
condition_code_to_procedure_code_l = pickle.load(open('pickles/coditioncode_to_listofprocedurescode.pickle', 'rb'))
procedure_code_to_name = pickle.load(open('pickles/procedurecode_to_procedurename.pickle', 'rb'))
means=pickle.load(open('pickles/means_coditioncode_observationcode.pickle','rb'))
deviations=pickle.load(open('pickles/derivation_coditioncode_observationcode.pickle','rb'))
observationname_to_code=pickle.load(open('pickles/observationsname_to_code.pickle','rb'))
procedurecode_to_cost=pickle.load(open('pickles/procedurecode_to_cost.pickle','rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Healthcheckup',methods=['GET'])
def Healthcheckup():
    return render_template('Healthcheckup.html')

@app.route('/Treatmentplanner',methods=['GET'])
def Treatmentplanner():
    return render_template('Treatmentplanner.html')

@app.route('/Healthcheckup/predict',methods=['POST'])
def Healthcheckuppredict():
    s = [str(x) for x in request.form.values()]
    if s[0] == "None":
        return render_template('Healthcheckup.html', prediction_text="No Description choosen.")   

    # Description to code
    try:
        desc_code = condition_desc_to_code[s[0]]
    except KeyError:
        return render_template('Healthcheckup.html', prediction_text="Record not found")

    sum_prob=0.0
    cnt_vitals=0
    extreme_vitals=[]
    vitals_loaded=0
    if s[3] != "":
        observation="Body Height"
        vitals_loaded=1
        
    if s[4] != "":
        observation="Body Weight"
        vitals_loaded=1
      
    if s[5] != "":
        observation="Diastolic Blood Pressure"
        vitals_loaded=1
        observationcode=observationname_to_code[observation]
        if desc_code in list(means.keys()):
            if observationcode in list(means[desc_code].keys()):
                mean=means[desc_code][observationcode]
                deviation=deviations[desc_code][observationcode]
                if deviation!=0.0:
                    prob=norm.pdf(float(s[5]), mean,deviation)/norm.pdf(mean, mean,deviation)
                    sum_prob=sum_prob+prob
                    cnt_vitals=cnt_vitals+1
                    if(prob>=0.8):
                        extreme_vitals.append(observation)
    
    if s[6] != "":
        observation="Systolic Blood Pressure"
        vitals_loaded=1
        observationcode=observationname_to_code[observation]
        if desc_code in list(means.keys()):
            if observationcode in list(means[desc_code].keys()):
                mean=means[desc_code][observationcode]
                deviation=deviations[desc_code][observationcode]
                if deviation!=0.0:
                    prob=norm.pdf(float(s[6]), mean,deviation)/norm.pdf(mean, mean,deviation)
                    sum_prob=sum_prob+prob
                    cnt_vitals=cnt_vitals+1
                    if(prob>=0.8):
                        extreme_vitals.append(observation)

    if s[7] != "":
        observation="Heart rate"
        vitals_loaded=1
        observationcode=observationname_to_code[observation]
        if desc_code in list(means.keys()):
            if observationcode in list(means[desc_code].keys()):
                mean=means[desc_code][observationcode]
                deviation=deviations[desc_code][observationcode]
                if deviation!=0.0:
                    prob=norm.pdf(float(s[7]), mean,deviation)/norm.pdf(mean, mean,deviation)
                    sum_prob=sum_prob+prob
                    cnt_vitals=cnt_vitals+1
                    if(prob>=0.8):
                        extreme_vitals.append(observation)

    if s[8] != "":
        observation="Respiratory rate"
        vitals_loaded=1
        observationcode=observationname_to_code[observation]
        if desc_code in list(means.keys()):
            if observationcode in list(means[desc_code].keys()):
                mean=means[desc_code][observationcode]
                deviation=deviations[desc_code][observationcode]
                if deviation!=0.0:
                    prob=norm.pdf(float(s[8]), mean,deviation)/norm.pdf(mean, mean,deviation)
                    sum_prob=sum_prob+prob
                    cnt_vitals=cnt_vitals+1
                    if(prob>=0.8):
                        extreme_vitals.append(observation)

    if s[9] != "":
        observation="Hemoglobin A1c/Hemoglobin.total in Blood"
        vitals_loaded=1
        observationcode=observationname_to_code[observation]
        if desc_code in list(means.keys()):
            if observationcode in list(means[desc_code].keys()):
                mean=means[desc_code][observationcode]
                deviation=deviations[desc_code][observationcode]
                if deviation!=0.0:
                    prob=norm.pdf(float(s[9]), mean,deviation)/norm.pdf(mean, mean,deviation)
                    sum_prob=sum_prob+prob
                    cnt_vitals=cnt_vitals+1
                    if(prob>=0.8):
                        extreme_vitals.append(observation)

    if cnt_vitals==0:
        return render_template('Healthcheckup.html', prediction_text="We can't predict based on these observations, need appropriate observations.")
    
    if vitals_loaded==1:
        sum_prob=sum_prob/cnt_vitals
        if len(extreme_vitals)==0:
            sum_prob=sum_prob*100
            sum_prob=int(sum_prob)
            sum_prob=100-sum_prob
            output="Based on these observation, you are "+str(sum_prob)+"% healthy."+'\n'+'\n'+"Stay healthy!"
            if s[1]!="" and s[2]!="":
                lat=float(s[1])
                lon=float(s[2])
                nearestorgdetails=nearest(lat,lon)
                output=output+'\n'+'\n'
                output=output+"You can contact the nearest hospital "
                output=output+nearestorgdetails["Name"]+'\n'+'\n'
                output=output+"You can also physically visit there at "+nearestorgdetails["ADDRESS"]
            return render_template('Healthcheckuphealthy.html', prediction_text1=output)
        else:
            output="Emergency!" +'\n'+'\n'+"You are in critical condtion."+'\n'+'\n'
            output=output+"Get your "
            for item in extreme_vitals:
                output=output + item+" "
            output=output+"checked urgently!"
            if s[1]!="" and s[2]!="":
                lat=float(s[1])
                lon=float(s[2])
                nearestorgdetails=nearest(lat,lon)
                output=output+'\n'+'\n'
                # nearestorgdetails = pickle.load(open('nearestorgdetails.pickle', 'rb'))
                output=output+"You can contact the nearest hospital "
                output=output+nearestorgdetails["Name"]+"."+'\n'+'\n'
                output=output+"You can also physically visit there at "+nearestorgdetails["ADDRESS"]+"."
            return render_template("Healthcheckupcritical.html",prediction_text2=output)

    return render_template("Healthcheckup.html")

@app.route('/Treatmentplanner/predict',methods=['POST'])
def Treatmentplannerpredict():
    s = [str(x) for x in request.form.values()]
    if s[0] == "None":
        return render_template('Treatmentplanner.html', prediction_text="No Description choosen.")   

    # Description to code
    try:
        desc_code = condition_desc_to_code[s[0]]
    except KeyError:
        return render_template('Treatmentplanner.html', prediction_text="Record not found")

    # Description code to careplan
    try:
        careplan_code_list = condition_code_to_careplan_code[desc_code]
        careplan = ""
        if len(careplan_code_list):
            careplan+="Recommended careplan: "
            for i, c_code in enumerate(careplan_code_list):
                careplan += careplan_code_to_careplan_desc[c_code]
                if i == len(careplan_code_list)-1:
                    careplan += '\n'
                else:
                    careplan += ", "
    except KeyError:
        careplan = ""

    # Description code to procedure codes
    try:
        procedure_code_list = condition_code_to_procedure_code_l[desc_code]
    except KeyError:
        return render_template('Treatmentplanner.html', prediction_text=careplan+'\n'+"No procedures expected.")

    procedures = ""
    procedures+="Expected procedures are: "
    for i, p_code in enumerate(procedure_code_list):
                procedures += str(procedure_code_to_name[p_code])
                if i == len(procedure_code_list)-1:
                    procedures += '\n'
                else:
                    procedures += ", "

    ## obtain cost of each procedure -----> To be upated
    cost_procedures=[]
    total_cost=0.0
    for item in procedure_code_list:
        cost_procedures.append(float(procedurecode_to_cost[item]))
        total_cost=total_cost+float(procedurecode_to_cost[item])
    
    output="Total expected cost for all the procedures is: Rs."+str(int(total_cost))+'\n'
    if s[1] != "":
        company = s[1]
        coverage = return_expected_coverage_of_company(company, desc_code, procedure_code_list, cost_procedures)
        coverage = int(coverage)
        temp = "Expected coverage of your company is: Rs."
        temp =temp+ str(coverage)
        output = output + temp
    else:
        best_company = best_insurance_company(desc_code, procedure_code_list, cost_procedures)
        temp = "Best insurance company for you is: "
        temp += str(best_company)
        output = output + temp  

    return render_template('Treatmentplanner.html', prediction_text=careplan+procedures+output)

if __name__ == "__main__":
    app.run(debug=True)

