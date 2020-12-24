from data import search, find_total_state, find_total_district, get_country_data

dict_state, dict_district = {}, {}
full_dict_state, full_dict_district = {}, {}


from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def home():
	if request.method == 'POST':
		given_input = request.form['given_input']
		dict_state_search_found, dict_district_search_found = search(given_input)
		l_state = len(list(i for i in dict_state_search_found.keys()))
		l_district = len(list(i for i in dict_district_search_found.keys()))
		return render_template('home.html', country_data=get_country_data(), l_state=l_state, l_district=l_district,given_input=given_input,dict_state=dict_state_search_found, dict_district=dict_district_search_found, title='home', data=True)
	return render_template('home.html', country_data=get_country_data(),title='home', data=False)

@app.route('/state', methods=['POST', 'GET'])
def state():
	if request.method == 'POST':
		given_input = request.form['given_input']
		dict_state_search_found, dict_district_search_found = search(given_input)
		l_state = len(list(i for i in dict_state_search_found.keys()))
		return render_template('state.html', l_state=l_state, given_input=given_input,dict_state=dict_state_search_found, title='state', full_dict_state=find_total_state(), data=True)
	return render_template('state.html', title='state', full_dict_state=find_total_state(), data=False)

@app.route('/district', methods=['POST', 'GET'])
def district():
	if request.method == 'POST':
		given_input = request.form['given_input']
		dict_state_search_found, dict_district_search_found = search(given_input)
		l_district = len(list(i for i in dict_district_search_found))
		return render_template('district.html',  l_district=l_district, given_input=given_input, dict_district=dict_district_search_found, title='district', full_dict_district=find_total_district(), data=True)
	return render_template('district.html', title='district', full_dict_district=find_total_district(), data=False)

if __name__ == '__main__':
	app.run(debug=True)
