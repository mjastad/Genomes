import models

#Create a demo user in the db for users without a 23andMe account
def create_demo_user():
    #check to see if demo user already exists in the db
    if models.db_session.query(models.User).filter(models.User.id=='demo_id').first() is None:
        #hard code the demo user's genome data
        genome_data = {
            'rs12913832': "GG",
            'rs1799971': 'AA',
            'rs1800955': 'CT',
            'rs806380': 'AG'
        }
        #hard code the demo user's relatives
        demo_relatives = [{
            'first_name': "Aodh",
            'last_name': "O'Donnell",
            'sex': "Male",
            'residence': "South Carolina",
            'similarity': 0.25,
            'maternal_side': False,
            'paternal_side': True,
            'birth_year': 1977,
            'relationship': "Brother",
            "birthplace": "United States",
            "ancestry": "Northwestern Europe",
            "picture_url": "https://goo.gl/lgh849"
            },
            {
            'first_name': "Ruarc",
            'last_name': "O'Donnell",
            'sex': "Male",
            'residence': "North Carolina",
            'similarity': 0.12,
            'maternal_side': False,
            'paternal_side': True,
            'birth_year': 1944,
            'relationship': "1st Cousin",
            "birthplace": "United States",
            "ancestry": "Northwestern Europe",
            "picture_url": "https://goo.gl/lgh849"
            },        
            {
            'first_name': "Maximus",
            'last_name': "Bundletreat",
            'sex': "Male",
            'residence': "New Jersey",
            'similarity': 0.125,
            'maternal_side': True,
            'paternal_side': False,
            'birth_year': 1974,
            'relationship': "1st Cousin",
            "birthplace": "United States",
            "ancestry": "Northwestern Europe",
            "picture_url": "https://goo.gl/lgh849"
            },
            {
            'first_name': "Quinci",
            'last_name': "Peachfuzz",
            'sex': "Female",
            'residence': "Georgia",
            'similarity': 0.0128,
            'maternal_side': True,
            'paternal_side': False,
            'birth_year': 1966,
            'relationship': "4th-6th Cousin",
            "birthplace": "United States",
            "ancestry": "Northwestern Europe",
            "picture_url": "https://goo.gl/lgh849"
            },
            {
            'first_name': "Wilder B.",
            'last_name': "Shick-Groundswell",
            'sex': "Male",
            'residence': "Louisiana",
            'similarity': 0.25,
            'maternal_side': False,
            'paternal_side': True,
            'birth_year': 1939,
            "birthplace": "France",
            "ancestry": "Northwestern Europe",
            'relationship': "Brother",
            "picture_url": "https://goo.gl/lgh849"
            },
            {
            'first_name': "Juniper",
            'last_name': "Kinglsey",
            'sex': "Male",
            'residence': "North Carolina",
            'similarity': 0.0134,
            'maternal_side': True,
            'paternal_side': False,
            'birth_year': 1955,
            "birthplace": "France",
            "ancestry": "Northwestern Europe",
            'relationship': "4th Cousin",
            "picture_url": "https://goo.gl/lgh849"
            },
            {
            'first_name': "Casseopeia",
            'last_name': "Middlemist-Gilbralter",
            'sex': "Female",
            'residence': "North Carolina",
            'similarity': 0.002,
            'maternal_side': False,
            'paternal_side': True,
            'birth_year': 1978,
            "birthplace": "Canada",
            "ancestry": "Northwestern Europe",
            'relationship': "Distant Relative",
            "picture_url": "https://goo.gl/lgh849"
            },
            {
            'first_name': "Andromeda",
            'last_name': "Middlemist-Gilbralter",
            'sex': "Female",
            'residence': "North Carolina",
            'similarity': 0.002,
            'maternal_side': False,
            'paternal_side': True,
            'birth_year': 1978,
            "birthplace": "Canada",
            "ancestry": "Northwestern Europe",
            'relationship': "Distant Relative",
            "picture_url": "https://goo.gl/lgh849"
        }]
        #Create demo user and all demo user's associated relatives
        demo_user = models.User('demo_id', None, 'Lilly', 'Demo', None, None, None, None, genome_data)
        for relative in demo_relatives:
            #Create a new relative with the information being passed from relatives_response
            new_relative = models.Relative(None, relative['first_name'], relative['last_name'], relative['sex'], relative['residence'], relative['similarity'], relative['maternal_side'], relative['paternal_side'], None, relative['birth_year'], relative['relationship'])
            # Appending each relative to the demo user's relative property
            demo_user.relatives.append(new_relative)
            models.db_session.add(new_relative)
        # Add the demo user to the database and commit it
        models.db_session.add(demo_user)
        models.db_session.commit()


#CreateNewUser will be called in server.py when a user logging in has not been found in database
def createNewUser(name_response, relatives_response, genotype_response, user_response):
    #Grab the dnaPairs at relative snps
    genome_data = genotype_response.json().pop()
    #Define the user's basic information
    user_first_name = name_response.json()['first_name']
    user_last_name = name_response.json()['last_name']
    user_id = genome_data['id']
    user_email = user_response.json()
    #Create a new user following the Users Model
    new_user = models.User(user_id, user_email['email'], user_first_name, user_last_name, None, None, None, None, genome_data)
    #iterate through list of relatives
    for relative in relatives_response.json()['relatives']:
        #Create a new relative with the information being passed from relatives_response
        new_relative = models.Relative(None, relative['first_name'], relative['last_name'], relative['sex'], relative['residence'], relative['similarity'], relative['maternal_side'], relative['paternal_side'], relative['picture_url'], relative['birth_year'], relative['relationship'], relative['birthplace'], relative['ancestry'])

        # Appending each relative to the user's relative property
        new_user.relatives.append(new_relative)
        models.db_session.add(new_relative)

    # Add the user to the database and commit it
    models.db_session.add(new_user)
    models.db_session.commit()


sample_snps = [
    {'rs_id':'rs12913832', 'dnaPair':'GG', 'outcome':'Makes your eyes blue'},
    {'rs_id':'rs12913832', 'dnaPair':'AA', 'outcome':'Makes your eyes brown, or less likely blue'},
    {'rs_id':'rs12913832', 'dnaPair':'AG', 'outcome':'Makes your eyes brown'},
    {'rs_id':'rs18050070', 'dnaPair':'CC', 'outcome':'Makes your hair read'},
    {'rs_id':'rs18050070', 'dnaPair':'CT', 'outcome':'Makes your hair read and increases response to anesthetics'},
    {'rs_id':'rs18050070', 'dnaPair':'TT', 'outcome':'Makes your hair read and increases response to anesthetics'},
    {'rs_id':'rs1799971', 'dnaPair':'AA', 'outcome':'Could make your children like alcohol'},
    {'rs_id':'rs1799971', 'dnaPair':'AG', 'outcome':'Responsible for your affinity for alcohol'},
    {'rs_id':'rs1799971', 'dnaPair':'GG', 'outcome':'Responsible for your affinity for alcohol'},
    {'rs_id':'rs806380', 'dnaPair':'AA', 'outcome':'Responsible for your strong predisposition for marijuana'},
    {'rs_id':'rs806380', 'dnaPair':'AG', 'outcome':'Responsible for your predisposition towards marijuana'},
    {'rs_id':'rs806380', 'dnaPair':'GG', 'outcome':'Responsible for your predisposition towards marijuana'},
    {'rs_id':'rs1800955', 'dnaPair':'CC', 'outcome':'Responsible for your tendency to novelty seek'},
    {'rs_id':'rs1800955', 'dnaPair':'CT', 'outcome':'Responsible for your tendency to novelty seek'},
    {'rs_id':'rs1800955', 'dnaPair':'TT', 'outcome':'Responsible for your tendency to novelty seek'},
    {'rs_id':'rs121908908', 'dnaPair':'CC', 'outcome':'Responsible for your low tolerance to pain'},
    {'rs_id':'rs121908908', 'dnaPair':'CG', 'outcome':'Responsible for your high tolerance to pain'},
    {'rs_id':'rs121908908', 'dnaPair':'GG', 'outcome':'Responsible for your high tolerance to pain'}
]

def createSnpsTable():
    for snp in sample_snps:
        new_snp = models.Snp(snp['rs_id'], snp['dnaPair'], snp['outcome'])
        models.db_session.add(new_snp)
        models.db_session.commit()
