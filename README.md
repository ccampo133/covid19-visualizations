# covid19-visualizations

[![](https://github.com/ccampo133/covid19-visualizations/workflows/Build%20master/badge.svg)](https://github.com/{owner}/{repo}/actions) 

Various visualizations for COVID-19 data. Accessible at https://covid19.ccampo.me.

Updates occur automatically every day at midnight GMT and on every push to master (see the GitHub Actions workflows for 
auto-update details).

Data provided by the [Johns Hopkins CSSE COVID-19 database](https://github.com/CSSEGISandData/COVID-19).

Visualizations inspired by http://nrg.cs.ucl.ac.uk/mjh/covid19/

# Requirements

Python 3.7

# Usage

I recommend using a [virtualenv](https://docs.python.org/3/library/venv.html):
                    
    $ python3 -m venv venv  
    # ...or just 'python', assuming that points to a Python 3.7 installation

Then activate it:

    $ source venv/bin/activate

Next, install from source:
    
    $ python setup.py develop
    
Then run the program from the command line:

    $ cov19vis
    Saved file: index.html
    Saved file: confirmed_select_countries_latest.png
    Saved file: confirmed_select_countries_2020_03_25_00_05.png

