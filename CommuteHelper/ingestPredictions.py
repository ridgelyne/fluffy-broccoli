import requests
import datetime
import pytz
import time

def ingestPredictions():
	#TODO: Put api key in configuration file
	headers = {
		'accept': 'text/event-stream',
		'x-api-key': 'bb73146176e64220b480f0af9f8b305a',
	}

	params = (
		('filter[route]', 'Red'),
		('include', 'vehicle'),
		('fields[shape]', 'name'),
	)

	try:
		# Read the streaming data from the MBTA
		response = requests.get('https://api-v3.mbta.com/predictions/', headers=headers, params=params, stream=True)

		# Save the streaming data to a file for later processing
		outfilename = 'red_line_predict_' + datetime.datetime.now(pytz.timezone('America/New_York')).strftime('%Y%m%d_%H%M%S') + '.txt'
		with open(outfilename, 'w') as outfile:
			for line in response.iter_lines():
				if line:
					msg = datetime.datetime.now(pytz.timezone('America/New_York')).strftime('%m/%d/%Y %H:%M:%S: ') + str(line) + '\n'
					outfile.write(msg)
	# If a problem with reading data, try again
	except requests.exceptions.RequestException as e:
		print(e)
		time.sleep(0.5) # Avoid exceeding the number of times the MBTA allows one to try to connect per minute
		ingestPredictions()
					
if __name__ == "__main__":
	ingestPredictions()