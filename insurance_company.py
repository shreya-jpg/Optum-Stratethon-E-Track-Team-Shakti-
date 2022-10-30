import pandas as pd 
import pickle
procedure_coverage_ratio = pickle.load(open('pickles/[companycode][conditioncode][procedurecode]_to_ratio.pickle', 'rb'))
insu_comp_to_code = pickle.load(open('pickles/insucompanyname_to_code.pickle', 'rb'))
code_to_insu_comp = pickle.load(open('pickles/insucompanycode_to_name.pickle', 'rb'))

def return_expected_coverage_of_company(company, condition_code, procedures_code, cost_procedures):
    expected_coverage = 0.0
    company_code = insu_comp_to_code[company]
    for i,p_code in enumerate(procedures_code):
        ratio = procedure_coverage_ratio[company_code][condition_code][p_code]
        expected_coverage += ratio * cost_procedures[i]

    return expected_coverage


def best_insurance_company(condition_code, procedures_code, cost_procedures): 
    coverage = []
    company = []
    for insu_comp in list(insu_comp_to_code.keys()):
        company_code = insu_comp_to_code[insu_comp]
        expected_coverage_of_this_company = 0.0
        for i,p_code in enumerate(procedures_code):
            ratio = procedure_coverage_ratio[company_code][condition_code][p_code]
            expected_coverage_of_this_company += ratio * cost_procedures[i]
        
        company.append(insu_comp)
        coverage.append(expected_coverage_of_this_company)
    
    maxi = coverage[0]
    index = 0

    for i in range(0,len(company)-1):
        if coverage[i] > maxi:
            index = i
            maxi = coverage[i]
        
    return company[index]+" (Covering upto Rs."+str(int(maxi))+")"
        


        
