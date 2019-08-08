import pandas as pd 
import datetime
import argparse

def get_year(num):
	if num < 2019:
		return num
	else:
		dt = datetime.date(1899, 12, 30) + datetime.timedelta(days=num)
		return dt.year 

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("input_file_name")
	parser.add_argument("output_file_name")
	args = parser.parse_args()
	data = pd.read_csv(args.input_file_name)
	data['RELEASE'] = data['RELEASE'].apply(get_year)
	data['LENGTH'] *= 1440
	data.drop(['#', 'RND'], axis=1, inplace=True)
	data.rename(columns={'POP.':'POP'}, inplace=True)
	data.to_csv(args.output_file_name, index=False)

if __name__ == '__main__':
	main()