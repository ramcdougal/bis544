from flask import Flask, render_template_string, jsonify, request
import pandas as pd 

my_template = """
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<script src="https://code.jquery.com/jquery-3.5.1.min.js"></script> 
<div id="myGraph"></div>
<div id="statename"></div>
<div id="statedata"></div>
<div>Data from the New York Times: https://github.com/nytimes/covid-19-data</div>
<script>
(
    fetch("/api/data")
    .then(response => response.json())
    .then(function (data) {Plotly.newPlot("myGraph", data, {
            "title": "Covid Cases by State",
            "geo": {
                "scope": "usa"
            }
        })
        myGraph.on("plotly_click", function(data) {
            let statename = data["points"][0]["location"];
            $("#statename").html(`<h1>You selected: ${statename}</h1>`);
            (
                fetch(`/api/statedata?state=${statename}`)
                .then(response => response.json())
                .then(function (data) {Plotly.newPlot("statedata", data)})
            )
        })
    })
)
</script>
"""

app = Flask(__name__)

# abbreviation list from https://gist.github.com/rogerallen/1583593 who disclaims copyright
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

covid = pd.read_csv("us-states.csv")

abbreviations = []

for state in covid.state:
    abbreviations.append(us_state_abbrev[state])

covid['ST'] = abbreviations

one_day = covid.loc[covid.date == '2020-11-30', :]
map_data = one_day[['ST', 'cases']].reset_index(drop = True)

my_data = [{
            "locations": map_data.ST.to_list(),
            "z": map_data.cases.to_list(),
            "locationmode": "USA-states",
            "type": "choropleth"
        }]

@app.route("/api/data")
def data():
    return jsonify(my_data)

@app.route("/api/statedata")
def statedata():
    state = request.args.get("state")
    my_state_data = covid[covid["ST"] == state]
    return jsonify([{
        "x": my_state_data.date.to_list(),
        "y": my_state_data.cases.to_list(),
        "type": "scatter"
    }])



@app.route("/")
def index():
    return render_template_string(my_template)


if __name__ == "__main__":
    app.run(debug=True)
