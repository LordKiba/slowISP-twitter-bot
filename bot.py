import os
import sys
import csv
import datetime
import time
import twitter

def test():

		#run speedtest-cli
		print ('running test')
		a = os.popen('speedtest.exe').read()
		print ('Parsing results')
		lines = a.split('\n')
		print (a)
		ts = time.time()
		date =datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

		#if speedtest could not connect set the speeds to 0
		if "Cannot" in a:
				p = '1000ms'
				d = '0.0Mbps'
				u = '0.0Mbps'
		#extract the values for ping down and up values
		else:
				s = lines[3] [13:255] #Ookla Server instance
				i = lines[4] [13:255] #ISP name
				p = lines[5] [16:255] # Ping
				d = lines[7] [14:255] # Download Speed
				u = lines[9] [14:255] # Upload Speed
				l = lines[10] [13:255] #Packet Loss
				r = lines[11] [13:255] # Result URL
		
		
		#extract jitter from string
		j = p[p.find("(")+1:p.find(")")].replace(' jitter', '').replace(' ', '')
		p = str(p.split('(')[0]).replace(' ', '')

		#extract data used on download from string
		du = d[d.find("(")+1:d.find(")")].replace('data used: ', '').replace(' ', '')
		d = str(d.split('(')[0])
		
		#extract data used on download from string
		uu = u[u.find("(")+1:u.find(")")].replace('data used: ', '').replace(' ', '')
		u = str(u.split('(')[0])


		print ('Writing data to log file')
		#save the data to file for local network plotting
		out_file = open('data.csv', 'a', newline='')
		writer = csv.writer(out_file)
		writer.writerow((ts*1000 , i, s, p, j, d, du, u, uu, l, r))
		out_file.close()
		
		#normalize numbers for tweet
		d = d.split(' ')[1]
		u = u.split(' ')[1]

		#init twitter
		TOKEN="{App_token}"
		TOKEN_KEY="{App_key}"
		CON_SEC="{Consumer_API_token}"
		CON_SEC_KEY="{Consumer_API_Key}"

		my_auth = twitter.OAuth(TOKEN,TOKEN_KEY,CON_SEC,CON_SEC_KEY)
		twit = twitter.Twitter(auth=my_auth)

		#try to tweet if speedtest fails to connect. wont work if the internet is down
		if "Cannot" in a:
				try:
						tweet="Hey @verizonfios @verizon @VerizonSupport \nWhy is my internet down? #fiosoutage #verizonfios #fiosfam"
						print (tweet)
						#twit.statuses.update(status=tweet)
				except:
						pass

		# tweet if down speed is less than 600Mbps
		elif eval(d)<600:
		
				print ("trying to tweet")
				try:
						tweet="Hey @verizonfios @verizon @VerizonSupport \nWhy is my internet speed " + str(int(eval(d))) + "Mbps down\\" + str(int(eval(u))) + "Mbps up when I pay for 1Gig symetric services? #verizonfios #speedtest #fiosfam  \n\n" + str(r)
						print (tweet)
					   # twit.statuses.update(status=tweet)
				except Exception as e:
						print (str(e))
						pass
		# tweet if up speed is less than 400Mbps
		elif eval(d)<400:
		
				print ("trying to tweet")
				try:
						tweet="Hey @verizonfios @verizon @VerizonSupport \nWhy is my internet speed " + str(int(eval(d))) + "Mbps down\\" + str(int(eval(u))) + "Mbps up when I pay for 1Gig symetric services? #verizonfios #speedtest #fiosfam  \n\n" + str(r)
						print (tweet)
					   # twit.statuses.update(status=tweet)
				except Exception as e:
						print (str(e))
						pass

		return
		
if __name__ == '__main__':
		test()
		print ('finished')
