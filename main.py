import pandas as pd
import EHRLink as ehrl
import os
import timeit

def main():
    df = pd.read_csv("test100.csv")

    # clean df for easy data transformation
    df = clean_df(df)

    transform_start = timeit.default_timer()
    # transform data to list of EHRLinks
    patient_list = parse_df(df)
    transform_end = timeit.default_timer()

    # analyze data and gather relevant data
    traverse_start = timeit.default_timer()
    result = analyze(patient_list)
    traverse_end = timeit.default_timer()

    transform_time = (transform_end - transform_start)
    traverse_time = (traverse_end - traverse_start)

    transform_time_per = (transform_end - transform_start) / len(df.index)
    traverse_time_per = (traverse_end - traverse_start) / len(patient_list)

    #export results to .csv
    path_to_export_csv = os.path.join(os.pathsep, os.getcwd(), 'result.csv')
    result.to_csv(path_to_export_csv, index=False)

    #export timer to .txt
    path_to_export_txt = os.path.join(os.pathsep, os.getcwd(), 'timer.txt')
    f = open('timer.txt', 'w')
    export_str = ("transform time: " + str(transform_time) + " (s), " +
                  str(transform_time_per) + " (s/row) \n" +
                  "traverse time: " + str(traverse_time) + " (s), " +
                  str(traverse_time_per) + " (s/patient) \n")

    f.write(export_str)
    f.close()

def clean_df(df):

    #sort by subject, visit, then starttime (reverse)
    df.sort_values(['subject_id', 'hadm_id','starttime'],
                   ascending=[True, True, False],
                   inplace=True)
    df = df.reset_index(drop=True)

    # add a column with a one row look ahead on hadm_id
    hadm_id_next = pd.concat([df['hadm_id'][1:], pd.Series([None])])
    hadm_id_next = hadm_id_next.reset_index(drop=True)
    hadm_id_next.name = 'hadm_id_next'

    # add a column with row look ahead on subject_id
    subject_id_next = pd.concat([df['subject_id'][1:], pd.Series([None])])
    subject_id_next = subject_id_next.reset_index(drop=True)
    subject_id_next.name = 'subject_id_next'

    return pd.concat([df,hadm_id_next,subject_id_next], axis=1)

def parse_df(df):

    patient_list = []

    isRowEndOfVisit = False
    isRowStartOfNewVisit = True

    curEhrLink = ehrl.EHRLink()

    for index, row in df.iterrows():

        if isRowStartOfNewVisit:

            # add discharge event
            curEhrLink.addDischargeNode(timeStamp=row.dischtime,
                                        visitId=row.hadm_id)

            # add death event if it has occurred for this visit id
            if row.deathflag == 1:
                curEhrLink.addDeathNode(timeStamp=row.deathtime,
                                        visitId=row.hadm_id)

        # add insulin admin event node
        curEhrLink.addInsulinAdminNode(startTime=row.starttime,
                                       endTime=row.endtime,
                                       amount=row.amount,
                                       visitId=row.hadm_id)

        if isRowEndOfVisit:

            curEhrLink.addCheckInNode(timeStamp=row.admittime,
                                      visitId=row.hadm_id)

            curEhrLink.addPatientDescriptor(patient_id=row.subject_id)

            if isRowNewPatient:
               patient_list.append(curEhrLink)
               curEhrLink = ehrl.EHRLink()


        isRowStartOfNewVisit = isRowEndOfVisit
        isRowEndOfVisit = row.hadm_id != row.hadm_id_next
        isRowNewPatient = row.subject_id != row.subject_id_next

    return patient_list

def analyze(patient_list):

    id_list = []
    visit_list = []
    death_list = []
    total_insulin_list = []

    for patient in patient_list:

        # initial variables and flags for data collection
        patient_id = None
        isCheckIn = False
        isCheckOut = False
        isDead = 0
        total_insulin = 0
        visits = 0

        # iterate through EhrLink and collect relevant data
        current = patient.head
        while current != None:
            data = current.getData()

            name = data.__class__.__name__

            if name == "PatientDescriptor":
                patient_id = data.id

            if name == "PatientDeath":
                isDead = 1

            if name == "InsulinAdmin":
                total_insulin += data.amount

            if name == "CheckOut":
                isCheckOut = True

            if name == "CheckIn":
                isCheckIn = True

            # if patient completes a visit
            if isCheckIn and isCheckOut:
                isCheckIn = False
                isCheckOut = False
                visits += 1

            current = current.getNext()

        id_list += [patient_id]
        visit_list += [visits]
        death_list += [isDead]
        total_insulin_list += [total_insulin]

    return make_into_df(id_list, visit_list, death_list, total_insulin_list)

def make_into_df(id_list, visit_list, death_list, total_insulin_list):
    result = pd.DataFrame(
        {'subject_id':id_list,
         'visits':visit_list,
         'deathflag':death_list,
         'total_insulin':total_insulin_list
        })
    return result

if __name__ == "__main__":
    main()