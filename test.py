def make_requests():
    import requests
    import json
    r = requests.get('https://api.covid19india.org/data.json')
    package_json = r.json()
    r2 = requests.get('https://api.covid19india.org/state_district_wise.json')
    package_json_district = r2.json()
    package_str = json.dumps(package_json, indent=2)
    package_str_district = json.dumps(package_json_district, indent=2)
    return package_json, package_json_district


def find_state(state_dict):
    new_state_dict = {}
    new_state_dict['statecode'] = state_dict['statecode']
    new_state_dict['state'] = state_dict['state']
    new_state_dict['confirmed'] = state_dict['confirmed']
    new_state_dict['active'] = state_dict['active']
    new_state_dict['recovered'] = state_dict['recovered']
    new_state_dict['deaths'] = state_dict['deaths']
    return new_state_dict


def find_district(district_dict):
    new_district_dict = {}
    # new_district_dict['state'] = district_dict['state']
    new_district_dict['confirmed'] = district_dict['confirmed']
    new_district_dict['active'] = district_dict['active']
    new_district_dict['recovered'] = district_dict['recovered']
    new_district_dict['deaths'] = district_dict['deceased']
    return new_district_dict


def search(given_input):
    from data import make_requests

    package_json, package_json_district = make_requests()

    dict_state_search_found = {}
    dict_district_search_found = {}

    for state in package_json['statewise']:
        if given_input.lower() == state['state'].lower() or given_input.lower() == state['statecode'].lower():
            print(state, '\n')
            dict_state_search_found[state['state']] = state
        elif given_input.lower() in state['state'].lower():
            dict_state_search_found[state['state']] = state
    # print(dict_state_search_found)
    # SAMPLE ELEMEMT : 'Maharashtra': {'active': '18381', 'confirmed': '24427', 'deaths': '921', 'deltaconfirmed': '0', 'deltadeaths': '0', 'deltarecovered': '0', 'lastupdatedtime': '12/05/2020 22:13:24', 'recovered': '5125', 'state': 'Maharashtra', 'statecode': 'MH', 'statenotes': '[10-May]<br>\n- Total numbers are updated to the final figure reported for 10th May. <br>\n- 665 cases added by MH govt. on 10th May due to data cleaning <br>\n- 143 cases added by MH govt. on 5th May due to data cleaning <br>\n- 796 cases added by MH govt. on 4th May due to data cleaning <br>'}

    for state_name in package_json_district.keys():
        for district in package_json_district[state_name]['districtData'].keys():
            if district.lower() == given_input.lower():
                dict_district_search_found[district] = package_json_district[state_name]['districtData'][district]
            elif given_input.lower() in district.lower():
                dict_district_search_found[district] = package_json_district[state_name]['districtData'][district]
    # print('\n\n', dict_district_search_found)
    # SAMPLE ELEMENT : 'North and Middle Andaman': {'notes': '', 'active': 0, 'confirmed': 1, 'deceased': 0, 'recovered': 1, 'delta': {'confirmed': 0, 'deceased': 0, 'recovered': 0}}
    return dict_state_search_found, dict_district_search_found


def find_total_state():
    from data import find_state
    from data import make_requests
    package_json, package_json_district = make_requests()
    full_dict_state = {}
    # full_dict_state['India'] = find_state('total')
    for i in package_json['statewise'][1:]:
        full_dict_state[i['state']] = find_state(i)

    return full_dict_state


def get_country_data():
    from data import find_state
    from data import make_requests
    package_json, package_json_district = make_requests()
    data_country = package_json['statewise'][0]
    data_country['state'] = 'India'
    return data_country


def find_total_district():
    from data import make_requests
    from data import find_district
    package_json, package_json_district = make_requests()
    full_dict_district = {}

    for state_name in package_json_district.keys():
        for district in package_json_district[state_name]['districtData'].keys():
            add_this = find_district(
                package_json_district[state_name]['districtData'][district])
            add_this['district'] = district
            full_dict_district[district] = add_this
    return full_dict_district


''' NOW LETS DO STATE GRAPH DATA!! '''


def state_graph_total():
    from matplotlib import pyplot as plt
    from matplotlib import dates as mpl_dates
    import requests
    import json
    from datetime import datetime
    r3 = requests.get('https://api.covid19india.org/v4/timeseries.json')
    package_json = r3.json()

    data = find_total_state()
    for i in data:

        # TOTAL LISTS
        state_list_x = []
        state_list_y = []
        state_recovered = []
        state_deceased = []

        # FREQUENCY LISTS
        state_list_y_f = []
        state_recovered_f = []
        state_deceased_f = []

        print(i)
        code = data[i]['statecode']
        a = 1
        initial = []
        for j in list(package_json[code]['dates']):
            initial.append(j)
            if len(initial) > 20 and initial[-2][5:7] != j[5:7]:
                initial[-1:]

            # print(j)
            # j = list(package_json[code]['dates'])[j]
            # print(j)
            # state_list_x.append(a)
            state_list_x.append(
                datetime(int(''.join(initial[-1][:4])), int(''.join(initial[-1][5:7])), int(''.join(initial[-1][8:]))))

            state_list_y.append(
                package_json[code]['dates'][initial[-1]]['total']['confirmed'])
            try:
                state_recovered.append(
                    package_json[code]['dates'][initial[-1]]['total']['recovered'])
            except:
                state_recovered.append(0)

            try:
                state_deceased.append(
                    package_json[code]['dates'][initial[-1]]['total']['deceased'])
            except:
                state_deceased.append(0)

            try:
                state_list_y_f.append(
                    package_json[code]['dates'][initial[-1]]['delta']['confirmed'])
            except:
                state_list_y_f.append(0)
            try:
                state_recovered_f.append(
                    package_json[code]['dates'][initial[-1]]['delta']['recovered'])
            except:
                state_recovered_f.append(0)

            try:
                state_deceased_f.append(
                    package_json[code]['dates'][initial[-1]]['delta']['deceased'])
            except:
                state_deceased_f.append(0)

            a += 10
        plt.plot_date(state_list_x, state_list_y, 'b',
                      label="Confirmed", linestyle='solid')
        # plt.gcf().autofmt_xdate()
        plt.plot_date(state_list_x, state_recovered, '-g',
                      label='Recovered', linestyle='solid')
        # plt.gcf().autofmt_xdate()
        plt.plot_date(state_list_x, state_deceased, 'r',
                      label='Deceased', linestyle='solid')
        # plt.gcf().autofmt_xdate()
        date_format = mpl_dates.DateFormatter('%b')
        plt.gca().xaxis.set_major_formatter(date_format)

        plt.xlabel('Days')
        plt.ylabel('Total Cases')
        plt.title(f'{i} covid cases')
        plt.legend()
        # plt.show()

        # from PIL import Image
        # img = Image.new("RGB", (800, 1280), (255, 255, 255))
        # img.save(f"{i}_total.png", "PNG")
        plt.savefig(f'./assets/graphs/{i}_total.png')
        plt.clf()

        plt.plot_date(state_list_x, state_list_y_f, 'b',
                      label="Confirmed")
        # plt.gcf().autofmt_xdate()
        plt.plot_date(state_list_x, state_recovered_f, '-g',
                      label='Recovered')
        # plt.gcf().autofmt_xdate()
        plt.plot_date(state_list_x, state_deceased_f, 'r',
                      label='Deceased')
        # plt.gcf().autofmt_xdate()
        date_format = mpl_dates.DateFormatter('%b')
        plt.gca().xaxis.set_major_formatter(date_format)

        plt.xlabel('Days')
        plt.ylabel('Total Cases')
        plt.title(f'{i} covid cases')
        plt.legend()
        # plt.show()

        # from PIL import Image
        # img = Image.new("RGB", (800, 1280), (255, 255, 255))
        # img.save(f"{i}_total.png", "PNG")
        plt.savefig(f'./assets/graphs/{i}_f.png')
        plt.clf()
        # break


state_graph_total()
