import datetime
import download_from_dropbox as down
import analyze as ana




# Replace with the path to the file in Dropbox and the local path where you want to save it
dropbox_path = '/應用程式/Glimp/GlicemiaMisurazioni.csv.gz'
local_path = '../data/meta/GlicemiaMisurazioni.csv.gz'
extract_path = f'../data/{datetime.datetime.today().strftime("%Y%m%d")}'
down.download_file_from_dropbox(dropbox_path, local_path)
down.extract_gz(local_path, extract_path)


data = ana.read_csv(extract_path)
data = ana.remove_inaccurate_data(data)
data = ana.separate_datetime_column(data)
ana.glucose_per_day(data)
ana.seperate_levels(data)
ana.standard_day(data)
data = ana.get_three_month_data(data)
ana.save_text_data(data)
print(f"total data number: {len(data)}")