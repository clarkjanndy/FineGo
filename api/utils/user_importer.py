import numpy as np
import pandas as pd

from django.contrib.auth.hashers import make_password
from django.core.files.uploadedfile import InMemoryUploadedFile
from api.models import User, Department
from api.utils.extras import convert_to_standard_date
from . exceptions import InvalidFileHeaderException

class UserImporter:
    
    ACCEPTED_HEADERS = {
        "lastname", 
        "firstname",
        "middlename", 
        "extension" , 
        "gender", 
        "address" , 
        "birthdate", 
        "course", 
        "year_level",
        "email" ,        
        "mobile"       
    }
    
    NA_VALUES = [" ", "", "N/A", "null"]
    
    def __init__(self, file: InMemoryUploadedFile) -> None:
        self.in_memory_file = file
        if not type(self.in_memory_file) == InMemoryUploadedFile:
            raise TypeError(f"Invalid type for file. Expected InMemoryUploadedFile, recieved {type(file)}")
        
        # detect if excel or csv
        self.file_type = self.in_memory_file.name.split(".")[-1].lower()
        if self.file_type not in  ['xls', 'xlsx', 'csv']:
            raise Exception('Unsupported file type. Must be one of ["xls", "xlsx", "csv].')
        
        self.dataframe = None
        
    def start_parsing(self):
        if self.file_type in ['xls', 'xlsx' ]:
            df = pd.read_excel(self.in_memory_file, na_values=self.NA_VALUES)
            
        elif self.file_type == 'csv':
            df = pd.read_csv(self.in_memory_file, na_values=self.NA_VALUES)
        
        if not self.ACCEPTED_HEADERS.issubset(df.columns):
            raise InvalidFileHeaderException(f'File header must contain all of the required headers.')
        
        df = df.replace(np.nan, None)
        self.dataframe = df
        return True
        
    def start_import(self):
        assert self.dataframe is not None, 'You must call .start_parsing() before .start_import()'
        
        created_rows, updated_rows, error_rows = [], [], []  
        rows = self.dataframe
        
        for index, row in rows.iterrows():
            try:
                department, _ = Department.objects.get_or_create(
                    abbreviation = row['course'], 
                    defaults = { "name": row['course']}
                )
                
                username = f"{row['email']}"
                password = username
                
                user, created = User.objects.update_or_create(
                    username = username,
                    email = row['email'],
                    student_id = row['student_id'],
                    first_name = row['firstname'],
                    middle_name = row['middlename'],
                    last_name = row['lastname'],
                    suffix = row['extension'],
                    defaults = {
                        "password": make_password(password),
                        "gender": row['gender'][0].upper(),
                        "address": row['address'],
                        "birthday": convert_to_standard_date(row['birthdate']),
                        "department": department,
                        "year_level": row['year_level'],
                        "mobile_number": row['mobile'],                        
                    }                          
                )        
                if created:
                    created_rows.append(index)
                else:
                    updated_rows.append(index)
                    
            except Exception as err:
                print(err)
                error_rows.append(index)
                
        return {
            "created": {
                "rows": created_rows,
                "count": len(created_rows)
            },
            "updated":{
                "rows": updated_rows,
                "count": len(updated_rows)
            },
            "errors":{
                "rows": error_rows,
                "count": len(error_rows)
            }
        }
                
                

        

