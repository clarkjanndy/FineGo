from datetime import datetime

def convert_to_standard_date(input_date):
    date_formats = ["%a %b %d %Y", "%d-%b-%y"]
    for date_format in date_formats:
        try:
            # Try to parse the input_date using the current format
            parsed_date = datetime.strptime(input_date, date_format).date()
            # Format the parsed date to the desired output format
            formatted_date = parsed_date.strftime('%Y-%m-%d')
            return formatted_date
        
        except ValueError:
            continue 
    return None