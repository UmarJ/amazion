import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from multiprocessing import Process, Queue, Pool, Manager
import threading
import sys

# use proxies in requests so as to proxy your request via a proxy server
# as some sites may block the IP if traffic generated by an IP is too high
proxies = {
  'http': 'http://134.119.205.253:8080',
  'https': 'http://134.119.205.253:8080',
}
startTime = time.time()
qcount = 0
products=[] #List to store name of the product
prices=[] #List to store price of the product
ratings=[] #List to store ratings of the product
images = []
no_pages = 20
Product_List = ["laptops","Headphones","scanners"]

def get_data(pageNo,q):  
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    
    r = requests.get("https://www.amazon.com/s?k=laptops&page="+str(pageNo), headers=headers)#, proxies=proxies)
    content = r.content
    soup = BeautifulSoup(content)
    #print(soup.encode('utf-8')) # uncomment this in case there is some non UTF-8 character in the content and
                 # you get error
    for product in Product_List:
        r = requests.get("https://www.amazon.com/s?k="+product+"&page="+str(pageNo), headers=headers)#, proxies=proxies)
        content = r.content
        soup = BeautifulSoup(content)
        for d in soup.findAll('div', attrs={'sg-row'}):
        	name = d.find('span', attrs={'class':'a-size-medium a-color-base a-text-normal'})
        	price = d.find('span', attrs={'class':'a-offscreen'})
        	rating = d.find('span', attrs={'class':'a-icon-alt'})
        	image = d.find('img',attrs = {'class':'s-image'})
        	#print(image)
        	all=[]
        	if name is not None and price is not None and rating is not None and image is not None:
        	    all.append(name.text)
        	    all.append(price.text)
        	    all.append(rating.text)
        	    all.append(image.attrs['src'])
        	'''else:
        	    all.append("unknown-product")
        	if price is not None:
        	    all.append(price.text)
        	else:
        	    all.append('$0')
        	if rating is not None:
            #print(rating.text)
        	    all.append(rating.text)
        	else:
        	    all.append('-1')

        	if image is not None:
            #print(rating.text)
        	    all.append(image.attrs['src'])
        	else:
        	    all.append('-1')            
		'''
        	#if name is not None:
        	 #   if price is not None:
        	  #      if rating is not None:
        	   #         if image is not None:
        	    #            all.append(name.text)
        	     #           all.append(price.text)
        	      #          all.append(rating.text)
        	       #         all.append(image.attrs['src'])
        	
        	q.put(all)
    #print("---------------------------------------------------------------") 
results = []
if __name__ == "__main__":
    m = Manager()
    q = m.Queue() # use this manager Queue instead of multiprocessing Queue as that causes error
    p = {}
    if sys.argv[1] in ['t', 'p']: # user decides which method to invoke: thread, process or pool
        for i in range(1,no_pages):
            if sys.argv[1] in ['t']:
                print("starting thread: ",i)
                p[i] = threading.Thread(target=get_data, args=(i,q))
                p[i].start()
            elif sys.argv[1] in ['p']:
                print("starting process: ",i)
                p[i] = Process(target=get_data, args=(i,q))
                p[i].start()
    # join should be done in seperate for loop 
    # reason being that once we join within previous for loop, join for p1 will start working
    # and hence will not allow the code to run after one iteration till that join is complete, ie.
    # the thread which is started as p1 is completed, so it essentially becomes a serial work instead of 
    # parallel
        for i in range(1,no_pages):
            p[i].join()
    else:
        pool_tuple = [(x,q) for x in range(1,no_pages)]
        with Pool(processes=8) as pool:
            print("in pool")
            results = pool.starmap(get_data, pool_tuple)
    
    while q.empty() is not True:
        qcount = qcount+1
        queue_top = q.get()
        if len(queue_top)!=0:
            print(len(queue_top))
            print(queue_top[0])
            products.append(queue_top[0])
            prices.append(queue_top[1])
            ratings.append(queue_top[2])
            images.append(queue_top[3])
    
    print("total time taken: ", str(time.time()-startTime), " qcount: ", qcount)
    #print(q.get())
    df = pd.DataFrame({'Product Name':products, 'Price':prices, 'Ratings':ratings, 'Image':images})
    print(df)
    df.to_csv('products.csv', index=False, encoding='utf-8')
