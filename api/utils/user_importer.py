import pandas as pd
from django.core.files.uploadedfile import InMemoryUploadedFile
from .exceptions import InvalidFileHeaderException

    
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
            df = pd.read_excel(self.in_memory_file)
            
        elif self.file_type == 'csv':
            df = pd.read_csv(self.in_memory_file)
        
        if not self.ACCEPTED_HEADERS.issubset(df.columns):
            raise InvalidFileHeaderException(f'File header must contain all of the required headers.')
        
        self.dataframe = df
        return True
        
    def start_import(self):
        assert self.dataframe is not None, 'You must call .start_parsing() before .start_import()'
        
        rows = self.dataframe
        for index, row in rows.iterrows():
            # import logic here nigga
            print(row)
            

        

