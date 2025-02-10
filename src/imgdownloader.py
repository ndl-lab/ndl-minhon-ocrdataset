import requests
import os
import pandas as pd
import time
import sys
import glob


if __name__ == '__main__':
    args = sys.argv
    mode=""
    if len(args)>=2:
        if args[1]=="v1":
           mode="v1"
        elif args[1]=="v2":
            mode="v2"
        else:
            print("The parameter must be 'v1 'or 'v2'.")
            sys.exit()
    else:
        mode="v2"
        print("The parameter must be 'v1 'or 'v2'.")
        #sys.exit()

    if mode=="v1":
        metadf=pd.read_csv("v1_metadata.csv",sep="\t",dtype=str)
        metadf=metadf[~metadf["Image URL"].isna()]
        keylist=[m1+"_"+m2 for m1,m2 in zip(metadf["Book ID"],metadf["File ID(NDL)"])]
        key2imgurl = dict(zip(keylist, metadf["Image URL"]))

        for bookdir in glob.glob(os.path.join("v1","*")):
            for filepath in glob.glob(os.path.join(bookdir, "*.json")):
                bookid=os.path.basename(bookdir)
                fileid=os.path.basename(filepath).split(".")[0]
                key=bookid+"_"+fileid
                if key in key2imgurl:
                    imgurl=key2imgurl[key]
                    #過去取得済みの画像をスキップする
                    if os.path.exists(os.path.join("img_v1", bookid, fileid+".jpg")):
                        continue
                    rawimg = requests.get(imgurl).content
                    os.makedirs(os.path.join("img_v1", bookid), exist_ok=True)
                    with open(os.path.join("img_v1", bookid, fileid+".jpg"), "wb") as fout:
                        fout.write(rawimg)
                        time.sleep(1)
    if mode=="v2":
        metadf=pd.read_csv("v2_metadata.csv",sep="\t",dtype=str)
        metadf=metadf[~metadf["Image URL"].isna()]
        keylist=[m1+"_"+m2+"_"+m3 for m1,m2,m3 in zip(metadf["Project ID"],metadf["Book ID"],metadf["File ID(Minna De Honkoku)"])]
        key2imgurl = dict(zip(keylist, metadf["Image URL"]))
        for projectdir in glob.glob(os.path.join("v2","*")):
            for bookdir in glob.glob(os.path.join(projectdir,"*")):
                for filepath in glob.glob(os.path.join(bookdir, "*.json")):
                    projectid=os.path.basename(projectdir)
                    bookid=os.path.basename(bookdir)
                    fileid=os.path.basename(filepath).split(".")[0]
                    key=projectid+"_"+bookid+"_"+fileid
                    if key in key2imgurl:
                        imgurl=key2imgurl[key]
                        #過去取得済みの画像をスキップする
                        if os.path.exists(os.path.join("img_v2",projectid, bookid, fileid+".jpg")):
                            continue
                        rawimg = requests.get(imgurl).content
                        os.makedirs(os.path.join("img_v2", projectid,bookid), exist_ok=True)
                        with open(os.path.join("img_v2",projectid, bookid, fileid+".jpg"), "wb") as fout:
                            fout.write(rawimg)
                            time.sleep(1)
