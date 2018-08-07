import pymysql
import requests
from bs4 import BeautifulSoup

baseUrl = "http://sports.39.net/cs/jsjh/sports/index_%d.html"
def get_inform(start):
	url = baseUrl % start
	lists = []
	html = requests.get(url)
	soup = BeautifulSoup(html.content, "html.parser")
	items = soup.find_all("span", "text")
	for i in items:
		ys = {}
		ys["title"] = i.find("a").text
		ys["link"] = i.find("a").get("href")
		#print(ys["title"])
		lists.append(ys)
	return lists

if __name__ == "__main__":
	db = pymysql.connect(host="localhost",user="root",password="1234",db="health",charset="utf8")
	cursor = db.cursor()
	cursor.execute("DROP TABLE IF EXISTS ys")
	createTab = """CREATE TABLE ys(
		id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
		title VARCHAR(50) NOT NULL,
		link VARCHAR(50) NOT NULL
	)"""
	cursor.execute(createTab)
	start = 1
	while (start < 50):
		lists = get_inform(start)
		for i in lists:
			sql = "INSERT INTO `ys`(`title`,`link`) VALUES(%s,%s)"
			try:
				cursor.execute(sql, (i["title"],i["link"]))
				db.commit()
			except:
				#print("faild")
				db.rollback()
		start += 1
		#print("finsh")
	db.close()