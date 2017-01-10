from math import pow
from math import sqrt

OUTPUT_NAME = "test data.csv"
STUD_PATH = "newData_STUD.txt"
STCR_PATH = "newData_STCR.txt"
STAI_PATH = "newData_STAI.txt"

fSTCR = open(STCR_PATH, "r")
global new_STCR # Used as a marker to indicate when a new student's data starts

fSTAI = open(STAI_PATH, "r")
global new_STAI # Used as a marker to indicate when a new student's data starts

class Student(object):
    def __init__(self, grade, gender, native_language, year_start, community_hours, OSSLT_eligible, OSSLT_status, OSSLT_completion_date, marks):
        if gender == "M":
            self.gender = 1
        elif gender == "F":
            self.gender = 0

        # NOTE: if gender is -1, data is set to be unused


        if OSSLT_eligible == "Eligible" and OSSLT_completion_date != "":
            self.grade = int(grade)
            self.year_start = int(year_start[0:4]) - (self.grade - 9)

            self.english_native = 1 # English is native language by default, becomes 0 if student takes an ESL course

            self.community_hours = community_hours

            self.OSSLT_first_attempt = 0 # 1 if student completes OSSLT on first attempt

            # sutract 1 to account for taking the test after new years
            if int(OSSLT_completion_date[0:4]) - self.year_start - 1 == 1:
                self.OSSLT_first_attempt = 1

            self.eng_avg = 0

            education_level_found = False 

            self.is_academic = 0
            self.is_applied = 0
            self.is_local = 0 # locally developed            
            self.is_IB = 0

            eng_courses = 0 # Number of english courses taken in grade 9
            for course in marks:
                date_completed = course[1]
                if course[1] != "N/A" and course[2] != "":
                    grade_avg = int(date_completed[0:4]) - self.year_start
                    if int(date_completed[5]) > 2: # Month is after February, thus completed first semester
                        grade_avg -= 1 # Account for new years
                    if grade_avg == 0:     
                        if course[0][0:3] == "ESL": # Checks if student is an taking ESL course by course code
                            self.english_native = 0
                            self.eng_avg += int(course[2])
                            eng_courses += 1
                            if not education_level_found: # If education level hasn't been decided yet, pick locally developed (Used in case student takes regular eng)
                                self.is_local = 1
                                eng_courses += 1
                                education_level_found = True
                        elif course[0][0:4] == "ENG1":
                            self.eng_avg = int(course[2])
                            eng_courses += 1
                            if course[0][-1] == "B":
                                self.is_IB = 1
                            elif course[0][4] == "L":
                                self.is_local = 1
                            elif course[0][4] == "P":
                                self.is_applied = 1
                            elif course[0][4] == "D":
                                self.is_academic = 1


            if eng_courses > 1: # Checks if ESL (since they take multiple eng courses in a year)
                self.eng_avg /= eng_courses # Take average

            if education_level_found: # If ESL was found first and another Eng course wasn't found, set to locally developed
                self.is_local = 1
                
            #Some students did not take grade 9 English, but have taken grade 10 applied english
            if (self.is_academic == 0 and self.is_applied == 0 
                and self.is_local == 0 and self.is_IB == 0):
                    self.is_applied = 1
                    
        else:
            self.gender = -1 # Throw out data since there are no OSSLT results

    def returnData(self):
        if self.gender != -1:
            data = [self.OSSLT_first_attempt, self.gender, self.english_native, self.eng_avg, self.is_academic, self.is_applied, self.is_local, self.is_IB]
        else:
            data = [-1] # Unneeded data
        return data

"""
Opens each data file and cycles through each line processing the data into the feature set
then put ito a csv.
"""
def gatherData(id, grade, gender, native_language, year_start):
    lines = [] # Data lines that belong to specified student
    done = False

    new_STCR = fSTCR.tell()
    fSTCR.seek(new_STCR) # Start at last read position

    while not done:
        current = fSTCR.readline().strip()
        if current.split("|")[0] == id:
            lines.append(current)
            new_STCR = fSTCR.tell() # Mark down last read position
        else:
            fSTCR.seek(new_STCR) # Start at last read position
            done = True

    studentAvgs = []
    marks = []

    for line in lines:
        info = []
        studentAvgs = line.split("|")
        if (studentAvgs[2] != ""):
            info = [studentAvgs[1], studentAvgs[2], studentAvgs[3], studentAvgs[4]] # Course code, date complete, average, credits
        else:
            info = [studentAvgs[1], "N/A", -1, -1] # -1 indicates incomplete

        marks.append(info)

    lines = []
    studentOther = []

    done = False

    new_STAI = fSTAI.tell()
    fSTAI.seek(new_STAI) # Start at last read position

    while not done:
        current = fSTAI.readline().strip()
        if current.split("|")[0] == id:
            lines.append(current)
            new_STAI = fSTAI.tell() # Mark down last read position
        else:
            fSTAI.seek(new_STAI) # Start at last read position
            done = True

    """
    STUDENT INFO INDEX (studentInfo[])
    -----------------------
    [8] Birthday
    [9] Grade
    [10] Gender
    [19] Native Language
    [21] School start date

    STUDENT AVERAGES INDEX (studentAvgs[])
    ---------------------------
    [1] Course code
    [2] Date completed
    [3] Average
    [4] Credits obtained
    [7] Category

    STUDENT OTHER INDEX (studentOther[])
    ---------------------------
    [0] Community hours
    [1] Literacy test requirements
    [2] Literacy test status
    [3] Reading results
    [4] Reading results date
    [5] Writing results
    [6] Writing results date
    """

    for i in range(len(lines)):
        studentOther.append(lines[i].split('|')[2].strip())

    data = Student(grade, gender, native_language, year_start, float(studentOther[0]), studentOther[2], studentOther[1], studentOther[4], marks)
    return data.returnData()

def main():
    
    with open(OUTPUT_NAME, "w") as output_file, open(STUD_PATH, "r") as id_list:
        index = 0
        total_data = []
        for line in id_list:
            student = line.split("|")
    
            """
            LABELS
            ---------------------------------------------------------------------------------------
            ["Database ID", "???", "Student ID", "OEN", "Last Name", "First Name", "Prefered L. Name", "Preferred F. Name",
            "Birthday", "Grade", "Gender", "Homeroom", "???", "???", "???", "???", "Grade Length", "Locker no.", "???",
            "Native Language", "Status", "School Start Date", "???", "School", "???", "Medical Info"]
            """
            data = gatherData(student[0], student[9], student[10], student[19], student[21])
            
            if len(data) > 1 and data[2] != -1: # Student must be eligible for the OSSLT to be used in dataset
                total_data.append([])            
                total_data[index].append(student[0])
                for data_point in data:
                    total_data[index].append(float(data_point))
                index += 1
            
        eng_mean = 0.0
        # Calculate the mean of all the averages
        for stud in total_data:
            eng_mean += stud[4] # Add up english averages
    
        N = len(total_data) # Number of data points
        eng_mean /= float(N)  
    
        variances_sum = 0 # Actually variances squared           
        # Calculate the standard deviation of all the averages
        for stud in total_data:
            variance = stud[4] - eng_mean
            variances_sum += pow(variance, 2)
        
        eng_stdev = sqrt(variances_sum / float(N - 1))
        
        # Z-score normalize the english averages
        for stud in total_data:
            stud[4] = (stud[4] - eng_mean) / eng_stdev
        
        # Printing to csv
        for stud in total_data:
            data_line = ""
            for data_point in stud:
                data_line += str(data_point) + ","
            output_file.write(data_line[:-1] + "\n") #[:-1] excludes final comma in the end  
        
    print("Finished processing:", N, "Students")
    print("Mean:", eng_mean, "STDEV:", eng_stdev)

if __name__ == '__main__':
    main()
