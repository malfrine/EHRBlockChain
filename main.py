import pandas as pd
import EHRLink as ehrl

def main():
    df = pd.read_csv("data.csv")

    #clean df for easy data transformation
    df = clean_df(df)

    patient_list = parse_df(df)

    analyze(patient_list)

def clean_df(df):

    #sort
    df.sort(['subject_id', 'hadm_id'],
            ascending=[1, 1],
            inplace=True)

    return df

def parse_df(df):

    patient_list = []
    cur_patient_id = None

    for row in df.iterrows():

        # if new patient_id:
            # add old EhrLink to patient_list
            # instantiate new EhrLink
            # add id to new EhrLink head

        # add admit event node
        # add insulin_admin event node
        # add death / discharge event node

        pass

    return patient_list

def analyze(patient_list):

    death = []
    insul_time = []
    insul_amount = []

    #foreach EhrLink in patient_list:
        # append last insul time - check_in time to insul_time
        # append last insul_amount to insul_amount
        #