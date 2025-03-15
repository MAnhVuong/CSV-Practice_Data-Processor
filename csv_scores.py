# Author   : Minh Anh Vuong
# Email    : minhanhvuong@umass.edu
# Spire ID : 34892350

import csv

def read_csv(fname):
    student_data = []
    try:
        with open(fname, 'r') as f:
            content = list(csv.reader(f))
            if len(content) == 0:
                return None
            for row in content:
                student_data.append({'name':row[0], 'section':row[1]})
                student_data[-1]['scores'] = [float(row[i]) for i in range (2,len(row))]
                student_data[-1]['average'] = round(sum(student_data[-1]['scores'])/10, 3)
    except:
        print(f'Error occurred when opening {fname} to read')
        return None
    return student_data

def write_csv(fname, student_data):
    try:
        with open(fname, 'w') as f:
            for row in student_data:
                combined = row['name'] + ',' + row['section'] + ','
                combined += ','.join(str(score) for score in row['scores'])
                f.write(combined + '\n')
    except:
        print(f'Error occurred when opening {fname} to write')
        return
    
def filter_section(student_data, section_name):
    return [student for student in student_data if student['section'] == section_name]

def filter_average(student_data, min_inc, max_exc):
    return [student for student in student_data if min_inc <= student['average'] < max_exc]

def split_section(fname):
    student_data = read_csv(fname)
    if student_data == None:
        return
    sections = set(student['section'] for student in student_data)
    inputfile = fname[:-4]
    for name in sections:
        write_csv(inputfile + '_section_' + name + '.csv', filter_section(student_data, name))
        
def get_stats(nums):
    mean = sum(nums) / len(nums)
    minimum = min(nums)
    maximum = max(nums)
    range = maximum - minimum
    std_dev = (sum([(n - mean)**2 for n in nums]) / len(nums)) ** (1/2)
    return mean, minimum, maximum, range, std_dev
    
def get_assignment_stats(student_data):
    return_list = []
    nums = [student['average'] for student in student_data]
    mean, minimum, maximum, range_nums, std_dev = get_stats(nums)
    return_list.append({'mean':mean, 'std_dev':std_dev, 'min':minimum, 'max':maximum, 'range':range_nums})
    for i in range(0, 10):
        nums = [student['scores'][i] for student in student_data]
        mean, minimum, maximum, range_nums, std_dev = get_stats(nums)
        return_list.append({'mean':mean, 'std_dev':std_dev, 'min':minimum, 'max':maximum, 'range':range_nums})
    return return_list

data = read_csv('students.csv')
write_csv('output.csv', data)
print(filter_average(data, 80.29, 85))
split_section('students.csv')
print(get_assignment_stats(data))