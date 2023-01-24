import shutil
from datetime import datetime
from OCRiser import *
from OCR_filtering import *
from SUTime_processing import *
from Entities_finder import *
from GROBID_generator import *

from bht_config import yml_settings

start_time = datetime.now()

sutime = SUTime(mark_time_ranges=True, include_range=True) # load sutime wrapper

papers_dir = yml_settings["BHT_PAPERS_DIR"]

for folders_or_pdf in os.listdir(papers_dir):
    folders_or_pdf_path = os.path.join(papers_dir, folders_or_pdf)
    if folders_or_pdf.endswith(".pdf"): # If '.pdf' on "Papers" folder --> paper not treated --> processing paper treatment.
        os.makedirs(os.path.join(papers_dir, folders_or_pdf.replace(".pdf", "")))  # create the directory under the same name than the paper.
        shutil.move(folders_or_pdf_path, os.path.join(papers_dir, folders_or_pdf.replace(".pdf", ""))) # move '.pdf' to his directory.
    pdf_paths = os.path.join(papers_dir, folders_or_pdf.replace(".pdf", ""))
    for pdf_files in os.listdir(pdf_paths): # processing treatment.
        if pdf_files.endswith(".pdf"):
            print(pdf_paths)
            if len(os.listdir(pdf_paths)) == 1: # Only 1 file (the pdf) --> directory never treated --> processing first treatment.
                PDF_file = os.path.join(pdf_paths,pdf_files)
                PDF_OCRiser(pdf_paths, PDF_file) # OCR the pdf file
                GROBID_generation(pdf_paths)  # generate the XML GROBID file
                filter(pdf_paths) # filter result of the OCR to deletes references, change HHmm4 to HH:mm, etc ...
                SUTime_treatement(pdf_paths, sutime) # SUTime read all the file and save its results in a file "res_sutime.json"
                SUTime_transform(pdf_paths) # transforms some results of sutime to complete missing, etc ... save results in "res_sutime_2.json"
                entities_finder(pdf_paths) # entities recognition and association + writing of HPEvent
            else: # case directory already treated: processing only after GROBID generation. (COMMENT TO DISABLE)
                filter(pdf_paths) # filter result of the OCR to deletes references, change HHmm to HH:mm, etc ...
                SUTime_treatement(pdf_paths,sutime) # SUTime read all the file and save its results in a file "res_sutime.json"
                SUTime_transform(pdf_paths) # transforms some results of sutime to complete missing, etc ... save results in "res_sutime_2.json"
                entities_finder(pdf_paths) # entities recognition and association + writing of HPEvent

end_time = datetime.now()
print("TOTAL ELAPSED TIME: ---"+str(end_time - start_time)+"---")
