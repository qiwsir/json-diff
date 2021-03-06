#! /usr/bin/env python
#coding:utf-8


from method import diffmethod

from dboption.mongodb import *

import json
import datetime
import time
import json_tools

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def diff():
    """
    find the difference between the two JSONs.
    """
    gene_last = [ ele["_id"] for ele in lastdb.find({},{'_id':1}) ]
    gene_new = [ ele["_id"] for ele in newdb.find({},{'_id':1}) ]
    
    geneid = diffmethod.OptLst(gene_last, gene_new)
    
    add_gene = geneid.addLst()              #the list consisting of the IDs in the new collection different from the IDs in the old one
    shared_gene = geneid.shareLst()         #the list consisting of the IDs in the new collection same as the IDs in the old one
    deleted_gene = geneid.deleLst()         #the list consisting of the IDs in the old collection but not in the new collection

    #insert the new values into the database.
    if add_gene:
        for i in add_gene:
            one_gene = newdb.find_one({"_id":i})
            db_change.insert({"gene_id":i,"changes":[{"stat":"new_gene","value":one_gene}],"lastdb":last_date,"newdb":new_date})
 
    #store the deleted IDs        
    if deleted_gene:
        for i in deleted_gene:
            one_gene = lastdb.find_one({"_id":i})
            db_change.insert({"gene_id":i,"changes":[{"stat":"delete"}],"lastdb":last_date,"newdb":new_date})
    
    #store the records in which the values have been changed
    if shared_gene:
        diff_gene = [i for i in shared_gene if cmp(lastdb.find_one({"_id":i},{"_id":0}),newdb.find_one({"_id":i},{"_id":0}))]   #the list of the IDs of the changed records
        print "diff_gene_list:",len(diff_gene)
    if diff_gene:
        for i in diff_gene:
            last_content = lastdb.find_one({"_id":i},{"_id":0})
            new_content = newdb.find_one({"_id":i},{"_id":0})
                
            diff = diffmethod.DiffJson(last_content, new_content)
            diff_lst = diff.diffDict()
            changes_value = diff.changesValue(diff_lst)
            db_change.insert({"gene_id":i, "changes":changes_value, "lastdb":last_date, "newdb":new_date })
         

def main():
    print ">>>Hi, I am Qiwei. Welcome to my website: www.itdiffer.com<<<"
    print "I am working like a horse. You may have a rest and I will send you the result after a while."
    diff()
    print "ok."


if __name__=="__main__":
    start = time.clock()
    main()
    print "The time I have spent is:"
    print (time.clock() - start)
