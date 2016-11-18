import json, urllib, sys

# print 'Number of arguments:', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv)


# This is the name of the single job you want to check
# Read input from cmdline <./main.py ntp will set job to ntp>
# job = str(sys.argv[2])
job = 'ntp'
job_name = 'forge-module_puppetlabs-' + job + '_init-merge_release'

# Function to return job names to inform end user what they can return this only returns linux
def return_job_names():
    data = urllib.urlopen("https://jenkins-modules.puppetlabs.com/api/json?tree=jobs[name]").read()
    output = json.loads(data)
    jobs = output['jobs']
    release_jobs = []
    for i in jobs:
        job_name = i['name']
        if '_init-merge_release' in job_name and 'forge-module_puppetlabs-' in job_name:
            release_jobs.append(job_name)
    # When going through all job names
    return release_jobs

# Function to return max build number as this should be release - Need to implement all numbers
def return_build_numbers(job_name):
    data = urllib.urlopen("https://jenkins-modules.puppetlabs.com/job/"+job_name+"/api/json?").read()
    output = json.loads(data)
    builds = output['builds']
    list=[]
    for i in builds:
        number = (i['number'])
        list.append(number)
        # build_number = max(list)
    # return str(build_number)
    return list

# Return SHA using build number and job name, this uses the max build number but in future will support a list
def return_release_SHA(build_number):
    data = urllib.urlopen("https://jenkins-modules.puppetlabs.com/job/" + job_name +"/"+ str(build_number) +"/api/json?").read()
    output = json.loads(data)
    try:
        SHA1 = output['actions'][5]['buildsByBranchName']['origin/release']['marked']['SHA1']
        return SHA1
    except:
        "No relevant branch"
    try:
        SHA1 = output['actions'][4]['buildsByBranchName']['origin/release']['marked']['SHA1']
        return SHA1
    except:
        "No relevant branch"
    try:
        SHA1 = output['actions'][3]['buildsByBranchName']['origin/release']['marked']['SHA1']
        return SHA1
    except:
        "No relevant branch"

# Returning the build status, this can be SUCESS, FAILURE etc
def return_release_result(build_number):
    data = urllib.urlopen("https://jenkins-modules.puppetlabs.com/job/" + job_name +"/"+ str(build_number) +"/api/json?").read()
    output = json.loads(data)
    build_result = (output.get('result'))
    return build_result

# Actually calling to print out the information possible (Singular)
if __name__ == '__main__':

    latest_build = max(return_build_numbers(job_name))
    jobs = return_job_names()
    SHA1 = return_release_SHA(latest_build)
    status = return_release_result(latest_build)
    print latest_build, job_name, SHA1, status


