import requests
import pandas as pd

from functools import lru_cache

# url = 'https://corona-api.com/countries'
# r = requests.get(url)
# json_response = r.json()['data']

# available_codes = [json_response[i]['code'] for i in range(len(json_response))]
# country_names = [json_response[i]['name'] for i in range(len(json_response))]

available_codes = ['AF', 'AL', 'AX', 'AS', 'DZ', 'AD', 'AO', 'AI', 'AG', 'AQ', 'AU', 'AT', 'BH', 'BD', 'BJ', 'BZ', 'AR', 'AM', 'BA', 'AW', 'AZ', 'BS', 'BN', 'BQ', 'BY', 'BB', 'IO', 'BM', 'BE', 'CM', 'BT', 'BO', 'KH', 'CF', 'BW', 'TD', 'BG', 'BV', 'BR', 'CC', 'CO', 'CA', 'BF', 'BI', 'CR', 'CV', 'KY', 'CK', 'CN', 'CW', 'CY', 'CX', 'CL', 'DO', 'KM', 'CG', 'CD', 'DM', 'GQ', 'CI', 'HR', 'CU', 'ER', 'CZ', 'DK', 'DJ', 'FJ', 'FO', 'SV', 'EG', 'TF', 'PF', 'EC', 'GH', 'EE', 'ET', 'DE', 'FK', 'FI', 'GD', 'FR', 'GP', 'GA', 'GF', 'GN', 'GM', 'GW', 'HN', 'GI', 'GE', 'GR', 'GL', 'VA', 'GT', 'ID', 'GG', 'IN', 'GU', 'IM', 'IL', 'GY', 'HK', 'HT', 'HM', 'JE', 'HU', 'IS', 'IR', 'IQ', 'IE', 'IT', 'JM', 'JP', 'KP', 'LV', 'LI', 'MG', 'MT', 'YT', 'MN', 'MM', 'NC', 'NU', 'JO', 'KR', 'LB', 'LT', 'MW', 'MH', 'KE', 'MX', 'KG', 'ME', 'KI', 'LR', 'LA', 'MO', 'LY', 'MV', 'MK', 'MR', 'ML', 'MU', 'NA', 'PK', 'MD', 'NZ', 'MA', 'NF', 'NP', 'PY', 'NE', 'MC', 'MZ', 'NL', 'NO', 'NG', 'PT', 'OM', 'RU', 'LC', 'SM', 'PW', 'SC', 'PE', 'SI', 'PR', 'SS', 'RW', 'SJ', 'MF', 'TW', 'ST', 'TG', 'SL', 'TR', 'SB', 'UA', 'ES', 'UY', 'SZ', 'VG', 'TJ', 'TK', 'TM', 'AE', 'UZ', 'VI', 'ZW', 'KZ', 'KW', 'LS', 'LU', 'MY', 'MQ', 'FM', 'MS', 'NR', 'NI', 'MP', 'PA', 'PN', 'RE', 'SH', 'VC', 'SN', 'SX', 'ZA', 'SD', 'CH', 'TH', 'TT', 'TV', 'US', 'VE', 'PG', 'PL', 'RO', 'KN', 'WS', 'RS', 'SK', 'GS', 'SR', 'SY', 'TL', 'TN', 'UG', 'UM', 'VN', 'PS', 'PH', 'QA', 'BL', 'PM', 'SA', 'SG', 'SO', 'LK', 'SE', 'TZ', 'TO', 'TC', 'GB', 'VU', 'WF', 'ZM', 'EH', 'YE']
country_names = ['Afghanistan', 'Albania', 'Åland Islands', 'American Samoa', 'Algeria', 'Andorra', 'Angola', 'Anguilla', 'Antigua and Barbuda', 'Antarctica', 'Australia', 'Austria', 'Bahrain', 'Bangladesh', 'Benin', 'Belize', 'Argentina', 'Armenia', 'Bosnia and Herzegovina', 'Aruba', 'Azerbaijan', 'Bahamas', 'Brunei ', 'Bonaire, Sint Eustatius and Saba', 'Belarus', 'Barbados', 'British Indian Ocean Territory', 'Bermuda', 'Belgium', 'Cameroon', 'Bhutan', 'Bolivia', 'Cambodia', 'CAR', 'Botswana', 'Chad', 'Bulgaria', 'Bouvet Island', 'Brazil', 'Cocos (Keeling) Islands', 'Colombia', 'Canada', 'Burkina Faso', 'Burundi', 'Costa Rica', 'Cape Verde', 'Cayman Islands', 'Cook Islands', 'China', 'Curaçao', 'Cyprus', 'Christmas Island', 'Chile', 'Dominican Republic', 'Comoros', 'Congo', 'DRC', 'Dominica', 'Equatorial Guinea', "Côte d'Ivoire", 'Croatia', 'Cuba', 'Eritrea', 'Czechia', 'Denmark', 'Djibouti', 'Fiji', 'Faroe Islands', 'El Salvador', 'Egypt', 'French Southern Territories', 'French Polynesia', 'Ecuador', 'Ghana', 'Estonia', 'Ethiopia', 'Germany', 'Falkland Islands', 'Finland', 'Grenada', 'France', 'Guadeloupe', 'Gabon', 'French Guiana', 'Guinea', 'Gambia', 'Guinea-Bissau', 'Honduras', 'Gibraltar', 'Georgia', 'Greece', 'Greenland', 'Vatican City', 'Guatemala', 'Indonesia', 'Guernsey', 'India', 'Guam', 'Isle of Man', 'Israel', 'Guyana', 'Hong Kong', 'Haiti', 'Heard Island and McDonald Islands', 'Jersey', 'Hungary', 'Iceland', 'Iran', 'Iraq', 'Ireland', 'Italy', 'Jamaica', 'Japan', "Korea, Democratic People's Republic of", 'Latvia', 'Liechtenstein', 'Madagascar', 'Malta', 'Mayotte', 'Mongolia', 'Myanmar', 'New Caledonia', 'Niue', 'Jordan', 'S. Korea', 'Lebanon', 'Lithuania', 'Malawi', 'Marshall Islands', 'Kenya', 'Mexico', 'Kyrgyzstan', 'Montenegro', 'Kiribati', 'Liberia', 'Laos', 'Macao', 'Libya', 'Maldives', 'North Macedonia', 'Mauritania', 'Mali', 'Mauritius', 'Namibia', 'Pakistan', 'Moldova', 'New Zealand', 'Morocco', 'Norfolk Island', 'Nepal', 'Paraguay', 'Niger', 'Monaco', 'Mozambique', 'Netherlands', 'Norway', 'Nigeria', 'Portugal', 'Oman', 'Russia', 'Saint Lucia', 'San Marino', 'Palau', 'Seychelles', 'Peru', 'Slovenia', 'Puerto Rico', 'South Sudan', 'Rwanda', 'Svalbard and Jan Mayen', 'Saint Martin', 'Taiwan', 'Sao Tome and Principe', 'Togo', 'Sierra Leone', 'Turkey', 'Solomon Islands', 'Ukraine', 'Spain', 'Uruguay', 'Swaziland', 'British Virgin Islands', 'Tajikistan', 'Tokelau', 'Turkmenistan', 'United Arab Emirates', 'Uzbekistan', 'U.S. Virgin Islands', 'Zimbabwe', 'Kazakhstan', 'Kuwait', 'Lesotho', 'Luxembourg', 'Malaysia', 'Martinique', 'Micronesia, Federated States of', 'Montserrat', 'Nauru', 'Nicaragua', 'Northern Mariana Islands', 'Panama', 'Pitcairn', 'Réunion', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Vincent Grenadines', 'Senegal', 'Sint Maarten', 'South Africa', 'Sudan', 'Switzerland', 'Thailand', 'Trinidad and Tobago', 'Tuvalu', 'USA', 'Venezuela', 'Papua New Guinea', 'Poland', 'Romania', 'Saint Kitts and Nevis', 'Samoa', 'Serbia', 'Slovakia', 'South Georgia and the South Sandwich Islands', 'Suriname', 'Syria', 'Timor-Leste', 'Tunisia', 'Uganda', 'United States Minor Outlying Islands', 'Vietnam', 'Palestine', 'Philippines', 'Qatar', 'Saint Barth', 'Saint Pierre Miquelon', 'Saudi Arabia', 'Singapore', 'Somalia', 'Sri Lanka', 'Sweden', 'Tanzania', 'Tonga', 'Turks and Caicos', 'UK', 'Vanuatu', 'Wallis and Futuna', 'Zambia', 'Western Sahara', 'Yemen']

get_code_from_name = dict(zip(country_names, available_codes))
get_name_from_code = dict(zip(available_codes, country_names))

@lru_cache
def construct_time_line(country_name : str) -> pd.DataFrame:
    
    if len(country_name) == 2:
        code = country_name.upper()
        if not code in available_codes:
            raise ValueError("Country code is not in the list !")

        url = 'https://corona-api.com/countries/'+ code +'?include=timeline'
    else:
        country_name = country_name.capitalize()
        if not country_name in country_names:
            raise ValueError("Country name is not in the list !")

        url = 'https://corona-api.com/countries/'+ get_code_from_name[country_name] +'?include=timeline'

    r = requests.get(url)
    json_response = r.json()['data']
    
    if not 'timeline' in json_response:
        raise ValueError("Timeline is not in json_reponse from corona-api.com")
    
    timeline = json_response['timeline']
    d = dict()
    
    #             date = datetime.strptime(date, '%Y-%m-%d')
    for i in range(len(timeline)-1, 0, -1):
        date = timeline[i]['updated_at'].split('T')[0]
        attrs = dict()
        attrs['new_confirmed'] = timeline[i]['new_confirmed']
        attrs['new_deaths'] = timeline[i]['new_deaths']

        d[date] = attrs
            
    df = pd.DataFrame.from_dict({'date' : d.keys(), 
                                   'confirmed': [list(d.values())[i]['new_confirmed'] for i in range(len(d.values()))],
                                   'deaths': [list(d.values())[i]['new_deaths'] for i in range(len(d.values()))]})

    df['date'] = pd.to_datetime(df['date'])

    return df