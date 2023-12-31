# SeekTruth.py : Classify text objects into two categories
#
# Hari_Galla(hgalla),Rohan_Radhakrishnan_Athlur(rathlur),Venkata Vishwanath Chittilla(vchitti)
#
# Based on skeleton code by D. Crandall, October 2021


import sys
import math 

def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")
            
    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

#Compute parameters function finds the count of each word in the review and also the individial probability of each word for both decpective and truthful classes seperately.
def computeParameters(inpData):

    #ClassDict holds two types of classes as the keys and the values contain all the words in reviews belonging to each class
    classDict={}
    classDict[inpData["classes"][0]]=[]
    classDict[inpData["classes"][1]]=[]

    #uniqueEleSet holds all the unique words present in the whole input file
    uniqueEleSet=set()

    for ele in inpData["objects"]:
        tempWords=ele.split(" ")
        tempSet=set(tempWords)
        uniqueEleSet.update(tempSet)
    
    #splitting each review based on space and then adding all the splitted words into the class dict of the corresponding class    
    for ele in range(len(inpData["labels"])):
        if inpData["labels"][ele]==inpData["classes"][0]:
            tempWords=inpData["objects"][ele].split(" ")
            classDict[inpData["classes"][0]].extend(tempWords)
        else:
            tempWords=inpData["objects"][ele].split(" ")
            classDict[inpData["classes"][1]].extend(tempWords)

    #countDict dictonary has two keys corresponding to the two class types and for each class type it holds the count of each word occuring in that class 
    countDict={}
    countDict[inpData["classes"][0]]={}
    countDict[inpData["classes"][1]]={}

    for ele in uniqueEleSet:
        
        countDict[inpData["classes"][0]][ele]=classDict[inpData["classes"][0]].count(ele)

    for ele in uniqueEleSet:
        
        countDict[inpData["classes"][1]][ele]=classDict[inpData["classes"][1]].count(ele)     

    #probDict dictonary also has two keys corresponding to the two class types and holds the probability of each word given that it belongs to a particular class
    #We also apply Laplace Smoothning to the probabilities so that one's with 0 probailities dont have a bias
    probDict={}
    probDict[inpData["classes"][0]]={}
    probDict[inpData["classes"][1]]={}

    for (key,value) in countDict[inpData["classes"][0]].items():
        probDict[inpData["classes"][0]][key]=math.log((value+1)/(len(classDict[inpData["classes"][0]])+(1*len(uniqueEleSet))))
    
    for (key,value) in countDict[inpData["classes"][1]].items():
        probDict[inpData["classes"][1]][key]=math.log((value+1)/(len(classDict[inpData["classes"][1]])+(1*len(uniqueEleSet))))


    #mainProb Dictonary holds the probability of each class type(Deceptive or truthful)
    mainProb={}

    mainProb[inpData["classes"][0]]=inpData['labels'].count(inpData["classes"][0])/(len(inpData['labels']))
    mainProb[inpData["classes"][1]]=inpData['labels'].count(inpData["classes"][1])/(len(inpData['labels']))

    return(probDict,mainProb)


def classifier(train_data, test_data):
    for pos in range(len(train_data["objects"])):
        train_data["objects"][pos]=train_data["objects"][pos].replace('~', '').replace("'", '').replace('`', '').replace('!', '').replace('@', '').replace('#', '').replace('$', '').replace('%', '').replace('^', '').replace('&', '').replace('*', '').replace('(', '').replace(')', '').replace('-', '').replace('_', '').replace('+', '').replace('=', '').replace('{', '').replace('}', '').replace('[', '').replace(']', '').replace(':', '').replace(';', '').replace('"', '').replace('<', '').replace(',', '').replace('>', '').replace('.', '').replace('?', '').replace('/', '').replace('|', '').replace('\\', '').lower() 
    
    for pos in range(len(test_data["objects"])):
        test_data["objects"][pos]=test_data["objects"][pos].replace('~', '').replace("'", '').replace('`', '').replace('!', '').replace('@', '').replace('#', '').replace('$', '').replace('%', '').replace('^', '').replace('&', '').replace('*', '').replace('(', '').replace(')', '').replace('-', '').replace('_', '').replace('+', '').replace('=', '').replace('{', '').replace('}', '').replace('[', '').replace(']', '').replace(':', '').replace(';', '').replace('"', '').replace('<', '').replace(',', '').replace('>', '').replace('.', '').replace('?', '').replace('/', '').replace('|', '').replace('\\', '').lower()
    
    #Here we get the output from the computeParameters wherein we get the individual probabilities of words and the probability of each class type
    (probDict,mainProb)=computeParameters(train_data)

    words=[]
    for ele in test_data["objects"]:
        words.append(ele.split(" "))
    

    #Applying Naive Bayes Theorem on each word , we calculate the probability it is the truth given the word & also the probability of deceptive given the word
    #We multiply the probability of all the words in the review with the corresponding class type probability

    spamProb=0
    notSpamProb=0
    resBool=[]
    for wrArr in words:
        spamProb=0
        notSpamProb=0
        for wr in wrArr:
            if wr in probDict[test_data["classes"][0]]: 
            
                spamProb=spamProb+(probDict[test_data["classes"][0]][wr])
        
        spamProb=spamProb+math.log(mainProb[test_data["classes"][0]])

        
        for wr in wrArr:
            if wr in probDict[test_data["classes"][1]]:

                notSpamProb=notSpamProb+(probDict[test_data["classes"][1]][wr])

                
        notSpamProb=notSpamProb+math.log(mainProb[test_data["classes"][1]])
            
        #Here we compare both the probabilities calculated.If the probability of truthful is grater than deceptive, then we assign the label Truthful else we assign the label as deceptive.
        if spamProb>notSpamProb:
            resBool.append(test_data["classes"][0])
        else:
            resBool.append(test_data["classes"][1])


    return resBool


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results= classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
