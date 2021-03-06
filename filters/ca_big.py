"""
Big California Districts.  Districts with more than 10,000 students in the 2009-2010 year
"""

ca_big_dist = {
    '0622710': 'Los Angeles Unified',
    '0634320': 'San Diego Unified',
    '0622500': 'Long Beach Unified',
    '0614550': 'Fresno Unified',
    '0612330': 'Elk Grove Unified',
    '0635310': 'Santa Ana Unified',
    '0634410': 'San Francisco Unified',
    '0634170': 'San Bernardino City Unified',
    '0607440': 'Capistrano Unified',
    '0609850': 'Corona-Norco Unified',
    '0614880': 'Garden Grove Unified',
    '0633840': 'Sacramento City Unified',
    '0634620': 'San Juan Unified',
    '0628050': 'Oakland Unified',
    '0633150': 'Riverside Unified',
    '0638640': 'Sweetwater Union High',
    '0613920': 'Fontana Unified',
    '0609030': 'Clovis Unified',
    '0638010': 'Stockton Unified',
    '0619540': 'Kern Union High',
    '0625800': 'Moreno Valley Unified',
    '0631530': 'Poway Unified',
    '0626370': 'Mt. Diablo Unified',
    '0602630': 'Anaheim Union High',
    '0634590': 'San Jose Unified',
    '0614400': 'Fremont Unified',
    '0625470': 'Montebello Unified',
    '0633860': 'Saddleback Valley Unified',
    '0608460': 'Chino Valley Unified',
    '0601332': 'Twin Rivers Unified',
    '0622230': 'Lodi Unified',
    '0628650': 'Orange Unified',
    '0600028': 'Temecula Valley Unified',
    '0632550': 'West Contra Costa Unified',
    '0611110': 'Desert Sands Unified',
    '0635130': 'San Ramon Valley Unified',
    '0631320': 'Pomona Unified',
    '0608610': 'Chula Vista Elementary',
    '0603630': 'Bakersfield City',
    '0684500': 'Irvine Unified',
    '0641160': 'Visalia Unified',
    '0632370': 'Rialto Unified',
    '0615240': 'Glendale Unified',
    '0642510': 'William S. Hart Union High',
    '0602820': 'Antelope Valley Union High',
    '0630660': 'Placentia-Yorba Linda Unified',
    '0641190': 'Vista Unified',
    '0611820': 'East Side Union High',
    '0608160': 'Chaffey Joint Union High',
    '0639420': 'Torrance Unified',
    '0609620': 'Compton Unified',
    '0616230': 'Grossmont Union High',
    '0629550': 'Palm Springs Unified',
    '0623610': 'Manteca Unified',
    '0609390': 'Colton Joint Unified',
    '0600014': 'Hesperia Unified',
    '0640150': 'Tustin Unified',
    '0611460': 'Downey Unified',
    '0628470': 'Ontario-Montclair Elementary',
    '0600029': 'Murrieta Valley Unified',
    '0616920': 'Hemet Unified',
    '0600027': 'Lake Elsinore Unified',
    '0627240': 'Newport-Mesa Unified',
    '0616740': 'Hayward Unified',
    '0613360': 'Fairfield-Suisun Unified',
    '0632070': 'Redlands Unified',
    '0609640': 'Conejo Valley Unified',
    '0628250': 'Oceanside Unified',
    '0629580': 'Palmdale Elementary',
    '0616325': 'Hacienda La Puente Unified',
    '0601620': 'Abc Unified',
    '0627690': 'Norwalk-La Mirada Unified',
    '0619260': 'Jurupa Unified',
    '0636840': 'Simi Valley Unified',
    '0603690': 'Baldwin Park Unified',
    '0602430': 'Alvord Unified',
    '0629940': 'Pasadena Unified',
    '0691135': 'Val Verde Unified',
    '0623340': 'Madera Unified',
    '0629490': 'Pajaro Valley Unified',
    '0612880': 'Escondido Union',
    '0602610': 'Anaheim City',
    '0602850': 'Antioch Unified',
    '0613890': 'Folsom-Cordova Unified',
    '0634880': 'San Marcos Unified',
    '0609070': 'Coachella Valley Unified',
    '0610290': 'Cupertino Union',
    '0600153': 'Alhambra Unified',
    '0626640': 'Napa Valley Unified',
    '0600047': 'Tracy Joint Unified',
    '0640980': 'Ventura Unified',
    '0629270': 'Oxnard Union High',
    '0606450': 'Burbank Unified',
    '0606390': 'Panama-Buena Vista Union',
    '0623160': 'Lynwood Unified',
    '0618060': 'Huntington Beach Union High',
    '0606810': 'Cajon Valley Union',
    '0629220': 'Oxnard',
    '0629850': 'Paramount Unified',
    '0633750': 'Rowland Unified',
    '0640740': 'Vallejo City Unified',
    '0635430': 'Santa Clara Unified',
    '0618390': 'Inglewood Unified',
    '0625130': 'Modesto City Elementary',
    '0625150': 'Modesto City High',
    '0600020': 'Pleasanton Unified',
    '0607970': 'Central Unified',
    '0600017': 'Apple Valley Unified',
    '0641280': 'Walnut Valley Unified',
    '0614760': 'Fullerton Joint Union High',
    '0642000': 'West Covina Unified',
    '0620880': 'Lancaster Elementary',
    '0600016': 'Upland Unified',
    '0605580': 'Santa Maria-Bonita',
    '0604440': 'Bellflower Unified',
    '0636972': 'Victor Valley Union High',
    '0610050': 'Covina-Valley Unified',
    '0600064': 'Porterville Unified',
    '0614730': 'Fullerton Elementary',
    '0600158': 'Turlock Unified',
    '0642480': 'Whittier Union High',
    '0633980': 'Salinas Union High',
    '0613140': 'Evergreen Elementary',
    '0643470': 'Yuba City Unified',
    '0602310': 'Alum Rock Union Elementary',
    '0608370': 'Chico Unified',
    '0626910': 'New Haven Unified',
    '0612960': 'Etiwanda Elementary',
    '0622110': 'Livermore Valley Joint Unified',
    '0640590': 'Vacaville Unified',
    '0634380': 'San Dieguito Union High',
    '0608130': 'Ceres Unified',
    '0620250': 'La Mesa-Spring Valley',
    '0600036': 'Natomas Unified',
    '0629610': 'Palo Alto Unified',
    '0629700': 'Palos Verdes Peninsula Unified',
    '0634710': 'San Lorenzo Unified',
    '0600013': 'Rocklin Unified',
    '0641040': 'Victor Elementary',
    '0635700': 'Santa Monica-Malibu Unified',
    '0627810': 'Oak Grove Elementary',
    '0635830': 'Santa Rosa High',
    '0621000': 'Las Virgenes Unified',
    '0625530': 'Monterey Peninsula Unified',
    '0615180': 'Gilroy Unified',
    '0607500': 'Carlsbad Unified',
    '0634920': 'San Mateo-Foster City',
    '0624600': 'Merced City Elementary',
    '0635250': 'Sanger Unified',
    '0630210': 'Perris Union High',
    '0623080': 'Lucia Mar Unified',
    '0603600': 'Azusa Unified',
    '0624660': 'Merced Union High',
    '0643080': 'Woodland Joint Unified',
    '0635970': 'Saugus Union',
    '0614430': 'Fremont Union High',
    '0612180': 'El Rancho Unified',
    '0614370': 'Franklin-Mckinley Elementary',
    '0612120': 'El Monte Union High',
    '0633630': 'Roseville Joint Union High'
}

ca_big_30_dist = {
    '0622710': 'Los Angeles Unified',
    '0634320': 'San Diego Unified',
    '0622500': 'Long Beach Unified',
    '0614550': 'Fresno Unified',
    '0612330': 'Elk Grove Unified',
    '0635310': 'Santa Ana Unified',
    '0634410': 'San Francisco Unified',
    '0634170': 'San Bernardino City Unified',
    '0607440': 'Capistrano Unified',
    '0609850': 'Corona-Norco Unified',
    '0614880': 'Garden Grove Unified',
    '0633840': 'Sacramento City Unified',
    '0634620': 'San Juan Unified',
    '0628050': 'Oakland Unified',
    '0633150': 'Riverside Unified',
    '0638640': 'Sweetwater Union High',
    '0613920': 'Fontana Unified',
    '0609030': 'Clovis Unified',
    '0638010': 'Stockton Unified',
    '0619540': 'Kern Union High',
    '0625800': 'Moreno Valley Unified',
    '0631530': 'Poway Unified',
    '0626370': 'Mt. Diablo Unified',
    '0602630': 'Anaheim Union High',
    '0634590': 'San Jose Unified',
    '0614400': 'Fremont Unified',
    '0625470': 'Montebello Unified',
    '0633860': 'Saddleback Valley Unified',
    '0608460': 'Chino Valley Unified',
    '0601332': 'Twin Rivers Unified'
}
