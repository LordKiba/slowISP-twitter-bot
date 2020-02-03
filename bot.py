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
        print (date,p, d, u)

        print ('Writing data to log file')
        #save the data to file for local network plotting
        out_file = open('data.csv', 'a')
        writer = csv.writer(out_file)
        writer.writerow((ts*1000,i,s,p,d,u,l,r))
        out_file.close()
		
		#normalize numbers for tweet
        d = d.split(' ')[1]
        u = u.split(' ')[1]

        #init twitter
        TOKEN=""
        TOKEN_KEY=""
        CON_SEC=""
        CON_SEC_KEY=""

        my_auth = twitter.OAuth(TOKEN,TOKEN_KEY,CON_SEC,CON_SEC_KEY)
        twit = twitter.Twitter(auth=my_auth)

        #try to tweet if speedtest fails to connect. wont work if the internet is down
        if "Cannot" in a:
                try:
                        tweet="Hey @verizonfios @verizon @VerizonSupport why is my internet down? #fiosoutage #verizonfios"
                        print (tweet)
                        twit.statuses.update(status=tweet)
                except:
                        pass

        # tweet if down speed is less than whatever I set
        elif eval(d)<750:
		
                print ("trying to tweet")
                try:
                        tweet="Hey @verizonfios @verizon @VerizonSupport why is my internet speed " + str(int(eval(d))) + "down\\" + str(int(eval(u))) + "up when I pay for 1000down\\1000up? "  + str(r) + " #verizonfios #speedtest"
                        print (tweet)
                        twit.statuses.update(status=tweet)
                except Exception as e:
                        print (str(e))
                        pass
        return
        
if __name__ == '__main__':
        test()
        print ('finished')
