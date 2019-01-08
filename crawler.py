import csv
import requests

from bs4 import BeautifulSoup

# contains software + hardware problems
# url = 'https://www.sih.gov.in/sih2019ProblemStatements?page='

# contains software problems
url ='https://www.sih.gov.in/sih2019ProblemStatements/QWxs/U29mdHdhcmU=/QWxs/QWxs/QWxs?page='


def get_soup(url, page):
	response = requests.get(url + str(page))

	data = response.text

	soup = BeautifulSoup(data, 'html.parser')

	assert soup.title.string == 'SIH'

	return soup


def get_problem_statement_div(soup):
	div = soup.find_all('div', id=lambda x : x and 'ViewProblemStatement' in x)

	return div


def get_div_tag(div, tag):
	children = div.find_all(tag)

	return children


def get_string(element):
	return element.string.strip().replace('\n', ' ').replace('\r', ' ') if element.string is not None else ' '


if __name__ == '__main__':
	csvfile = open('sih_ps.csv', 'w')

	writer = csv.writer(csvfile, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)

	pages = 33

	for page in range(1, pages):
		print(f"Crawling page {page}")
		soup = get_soup(url, page)

		problem_statement_div = get_problem_statement_div(soup)

		for div in problem_statement_div:
			"""	get parent of current element which contains
				company logo, name, problem statement popup, 
				number of submissions, technology bucket, complexity """
			parent = div.find_parent('tr')

			# get all the columns
			all_columns = get_div_tag(parent, 'td')

			# extract relevant information
			name = all_columns[1].string
			category = all_columns[8].string
			tech_bucket = all_columns[10].string
			complexity = all_columns[11].string

			# all <th> tags contain headings
			all_th = get_div_tag(div, 'th')

			# all <td> tags contain information about the problem statement
			all_td = get_div_tag(div, 'td')

			# _td = get_string(all_td[1:-1])

			problem_statement = get_string(all_td[0].find('div'))
			youtube_link = get_string(all_td[-1].find('a'))

			# final information to dump
			info = []
			info.append(name)
			info.append(tech_bucket)
			info.append(problem_statement)
			info.append(youtube_link)
			info.append(complexity)

			writer.writerow(info)