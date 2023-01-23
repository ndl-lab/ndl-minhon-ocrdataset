import sys
import os
import glob
import cv2
import json
if __name__ == '__main__':
    args = sys.argv
    mode=""
    if len(args)>=2:
        if args[1]=="v1":
           mode="v1"
        elif args[2]=="v2":
            mode="v2"
        else:
            print("The parameter must be 'v1 'or 'v2'.")
            sys.exit()
    else:
        print("The parameter must be 'v1 'or 'v2'.")
        #mode="v2"
        sys.exit()

    if mode=="v1":
        outputdir="honkoku_oneline_v1"
        os.makedirs(outputdir,exist_ok=True)
        for bookdir in glob.glob(os.path.join("img_v1","*")):
            for imgfilepath in glob.glob(os.path.join(bookdir, "*.jpg")):
                jsonfilepath=imgfilepath.replace(".jpg",".json").replace("img_v1","v1")
                img = cv2.imread(imgfilepath)
                with open(jsonfilepath, "r", encoding="utf-8") as jsonfile_open:
                    jsonfile_load = json.load(jsonfile_open)
                    for index,word in enumerate(jsonfile_load):
                        x0, y0 = word["boundingBox"][0]
                        x1, y1 = word["boundingBox"][1]
                        x2, y2 = word["boundingBox"][2]
                        x3, y3 = word["boundingBox"][3]
                        xmin = min([x0, x1, x2, x3])
                        xmax = max([x0, x1, x2, x3])
                        ymin = min([y0, y1, y2, y3])
                        ymax = max([y0, y1, y2, y3])
                        outtext=word["text"]
                        outputimgpath = os.path.join(outputdir, "{}_{}.jpg".format(
                        os.path.basename(bookdir) + "-" + os.path.basename(imgfilepath).split(".")[0], index))
                        outputtxtpath = outputimgpath.replace(".jpg", ".txt")
                        cv2.imwrite(outputimgpath, img[ymin:ymax, xmin:xmax])
                        with open(outputtxtpath, "w", encoding="utf-8") as wf:
                            wf.write(outtext)
    if mode=="v2":
        outputdir = "honkoku_oneline_v2"
        os.makedirs(outputdir, exist_ok=True)
        for projectdir in glob.glob(os.path.join("img_v2", "*")):
            for bookdir in glob.glob(os.path.join(projectdir, "*")):
                for imgfilepath in glob.glob(os.path.join(bookdir, "*.jpg")):
                    jsonfilepath = imgfilepath.replace(".jpg", ".json").replace("img_v2", "v2")
                    #print(imgfilepath)
                    img = cv2.imread(imgfilepath)
                    with open(jsonfilepath, "r", encoding="utf-8") as jsonfile_open:
                        jsonfile_load = json.load(jsonfile_open)
                        for index, word in enumerate(jsonfile_load):
                            x0, y0 = word["boundingBox"][0]
                            x1, y1 = word["boundingBox"][1]
                            x2, y2 = word["boundingBox"][2]
                            x3, y3 = word["boundingBox"][3]
                            xmin = min([x0, x1, x2, x3])
                            xmax = max([x0, x1, x2, x3])
                            ymin = min([y0, y1, y2, y3])
                            ymax = max([y0, y1, y2, y3])
                            outtext = word["text"]
                            outputimgpath = os.path.join(outputdir, "{}_{}.jpg".format(
                                os.path.basename(projectdir) + "-" +
                                os.path.basename(bookdir) + "-" + os.path.basename(imgfilepath).split(".")[0],index))
                            outputtxtpath = outputimgpath.replace(".jpg", ".txt")
                            cv2.imwrite(outputimgpath, img[ymin:ymax, xmin:xmax])
                            with open(outputtxtpath, "w", encoding="utf-8") as wf:
                                wf.write(outtext)
