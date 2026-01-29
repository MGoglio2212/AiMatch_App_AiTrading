
import os 
from pdf2jpg import pdf2jpg
import shutil 

input_folder = r"C:\\Progetti\\AIMatch\\Codes\\Streamlit_app\\Mail\\"
output_folder = r"C:\\Progetti\\AIMatch\\Codes\\Streamlit_app\\Mail_Images\\"
outputpath = ""
for ff in os.listdir(input_folder):
     filename = os.fsdecode(ff)
     print(filename)
     result = pdf2jpg.convert_pdf2jpg(input_folder + filename,outputpath, pages="ALL") 

     shutil.copy(filename + "_dir\\0_" + filename + ".jpg", output_folder + filename + ".jpg")
     shutil.rmtree(filename + "_dir")
