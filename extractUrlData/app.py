from flask import Flask, jsonify, request
from newspaper import Article
from langdetect import detect
from urllib.parse import urlparse
from iso639 import languages
import re

app = Flask(__name__)

@app.route('/api/extract', methods = ['POST'])
def index():
	print("Inside extraction")
	print(request)
	if not request.json or not 'url' in request.json:
		abort(400)
	url = request.json['url']
	article = Article(url)
	
	article.download()
	article.parse()
	
	print("Publish date:")
	print(article.publish_date)

	#authors of article
	authors = []
	print("Authors:")
	for x in article.authors:
		authors.append( x )
	
	content = []
	lines = article.text.split('\n')
	print("Article text:")
	for x in lines:
		if x != "AD":
			content.append(x)
	
	#text of article
	text = ''.join(content)
	# print(text)

	#title of article
	print("Article Title")
	title = article.title

	#hasImage in article
	print("Has Image")
	hasImage = 0
	if article.images:
		hasImage = 1

	#language of article
	print("Language of article")
	language = detect(text)

	#mainsite URL
	#find a better way than [4:]
	print("Main Site URL")
	mainSiteURL = (urlparse(url).netloc)[4:]

	return jsonify(
		authors = authors,
		text = text,
		title = title,
		hasImage = hasImage,
		language = (languages.get(alpha2 = language)).name,
		site_url = mainSiteURL,
		published = article.publish_date
	)

if __name__ == "__main__":
	app.run(debug=True)