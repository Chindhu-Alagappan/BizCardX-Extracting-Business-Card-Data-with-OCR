# BizCardX-Extracting-Business-Card-Data-with-EasyOCR
This is an open-source project repo which deals with extracting text data from business card using Easy OCR. A Streamlit GUI has been built with the ability to Upload image for extraction, Save them to the DB, Update the data stored and Delete the records.  

## Introduction
Optical Character Recognition (OCR) is a process of converting images of typed, hand-written or printed text format into the machine-encoded form. EasyOCR is a Python library for Optical Character Recognition (OCR) that allows you to easily extract text from image documents uploaded through GUI. Also,  it provides support for about 80+ languages.  

## Table of Contents
1. Pre-requisites
2. Technology Stacks 
3. Usage
4. Image Processing with EasyOCR  
5. Formatting the fields extracted
6. Building Streamlit GUI
   - BizCardX Tab
   - Upload Tab
   - View Tab
   - Update Tab
   - Delete tab
7. MySQL Table Schema
8. Further Improvements

## Pre-requsites
Install the following packages to run the project. 
```
pip install streamlit
pip install easyocr
pip install numpy
pip install mysql-connector-python
pip install Pillow
pip install pandas
```
## Technology Stack
- Python scripting 
- SQL - MySQL  
- Streamlit GUI development  
- EasyOCR  
- Data Extraction and Formatting  

## Usage
Clone the repo from the below mentioned link.  
[BizCardX-Extracting-Business-Card-Data-with-EasyOCR](https://github.com/Chindhu-Alagappan/BizCardX-Extracting-Business-Card-Data-with-OCR.git)  
Install packages from "requirement.txt"  
Run the streamlit application using `streamlit run .\BizCard.py`  
View the portal in your [localhost](http://localhost:8501/)  

## Image Processing with EasyOCR
Extracting text data from the business card is done using the below piece of code.  
```
reader = easyocr.Reader(['en'], gpu=False)
result = reader.readtext(np.array(image)) 
```
The resultant output consists of information such as the 4 co-ordinates [(x1,y1),(x2,y2),(x3,y3),(x4,y4)], text detected and the confidence level of detection.   

## Formatting the fields extracted
The extracted text has to be categorized and formatted into the following.  
1. Card_No - Business card number - *Image name must be in number format*
2. Name - Name of card holder
3. Role - Role of the person in the company
4. Company - Company name
5. Email - EmailId of the person
6. Phone - Contact number(s) of the person
7. Website - Website of the company
8. Address - Address of the company  

## Building Streamlit GUI
### BizCardX Tab
Contains basic information of the tool.  
[Image_1](https://github.com/Chindhu-Alagappan/BizCardX-Extracting-Business-Card-Data-with-OCR/blob/f33bb5f3c890e4791ebff5d48c7c88a58e8b5407/Snapshots%20-%20output/Image_1.png)

### Upload Tab
Provides the ability to upload image and view the extracted text in a readable from the image.    
If we wish to save to the database we can do so, by hitting the *Save* button.    
[Image_2](https://github.com/Chindhu-Alagappan/BizCardX-Extracting-Business-Card-Data-with-OCR/blob/f33bb5f3c890e4791ebff5d48c7c88a58e8b5407/Snapshots%20-%20output/Image_2.png)

### View Tab
View the data saved in the database - MySQL.    
[Image_3](https://github.com/Chindhu-Alagappan/BizCardX-Extracting-Business-Card-Data-with-OCR/blob/f33bb5f3c890e4791ebff5d48c7c88a58e8b5407/Snapshots%20-%20output/Image_3.png)

### Update Tab
Has the ability to choose the image data where the updation has to be made in the DB, by selecting the card number (ie) image name, field and new value to update. 
 [Image_4](https://github.com/Chindhu-Alagappan/BizCardX-Extracting-Business-Card-Data-with-OCR/blob/f33bb5f3c890e4791ebff5d48c7c88a58e8b5407/Snapshots%20-%20output/Image_4.png)

### Delete Tab
We can delete the records of the extracted image from the DB, through this tab, by providing the card number (ie) image name to delete.  
[Image_5](https://github.com/Chindhu-Alagappan/BizCardX-Extracting-Business-Card-Data-with-OCR/blob/f33bb5f3c890e4791ebff5d48c7c88a58e8b5407/Snapshots%20-%20output/Image_5.png)

## MySQL Table Schema  
**Table : User1**  
| Column Name | Data Type | Description |
| :---------- | :-------- | :---------- |
| Card_No | INT | Unique identifier to identify the images |
| Name | VARCHAR(255) | Name of card holder |
| Role | VARCHAR(255)  | Role of the person in the company |
| Company | VARCHAR(255) | Company name |
| Email | VARCHAR(255) | EmailId of the person |
| Phone | VARCHAR(255) | Contact number(s) of the person |
| Website | VARCHAR(255) | Website of the company |
| Address | TEXT | Address of the company |
| Image | LONGBOB | Originally Uploaded Image |

## Further Improvements 
The project can further be enhanced by securing the GUI application with user authentication and authorization. This will help multiple users to access the application in parallel, with atmost security and privacy of the images processed.  
If you encounter any issues or have suggestions for improvements, feel free to reach out.    

Email : *chindhual@gmail.com*    
LinkedIn : *https://www.linkedin.com/in/chindhu-alagappan-57605112a/*   
  
Thanks for showing interest in this repository ! 
