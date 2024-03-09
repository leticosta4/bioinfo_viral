from xml.dom import minidom
import pandas as pd

# Dicionário inicial vazio
dict_info = {
    'Sequence': [],
    'Locus': [],
    'Length': [],
    'Update date': [],
    'Creation date': [],
    'Pubmed accession number': [],
    'Country': [],
    'Host': [],  
    'Collection_date': [],
    'Nucleotide Sequence': []
}

dict_extra = {
    'Locus': [],
    'Pubmed accession number': []
}

with open("sequence.gbc.xml", "r") as file: 
    xml = minidom.parse(file) #parseando para criar o objeto xml dom

    general = xml.getElementsByTagName("INSDSeq")

    for i in range(len(general)):
        locus = general[i].getElementsByTagName("INSDSeq_locus")[0].firstChild.data
        length = general[i].getElementsByTagName("INSDSeq_length")[0].firstChild.data
        update_date = general[i].getElementsByTagName('INSDSeq_update-date')[0].firstChild.data
        creation_date = general[i].getElementsByTagName('INSDSeq_create-date')[0].firstChild.data

        qualifiers = {}
        qualifiers_names = general[i].getElementsByTagName("INSDQualifier_name")
        qualifiers_values = general[i].getElementsByTagName("INSDQualifier_value")

        temp_info = {
            'Sequence': i + 1,
            'Locus': locus,
            'Length': length,
            'Update date': update_date,
            'Creation date': creation_date,
            'Pubmed accession number': [], 
            'Country': qualifiers.get("country", ""),
            'Host': qualifiers.get("host", ""),
            'Collection_date': qualifiers.get("collection_date", ""),
            'Nucleotide Sequence': [] 
        }

        temp_extra = {
            'Locus': locus,
            'Pubmed accession number': []
        }

        #pegando os 3 qualificadores específicos que variam de acordo com sequencia
        for name, value in zip(qualifiers_names, qualifiers_values):
                qualifiers[name.firstChild.data] = value.firstChild.data.capitalize()
        
        for n in range(len(qualifiers_names)):
            v = n
            auxCountry = auxHost = auxCollec = qualifiers_names[n].firstChild.data
            existsCountry = existsHost = existsCollec = False
            while(existsCountry != True):
                if auxCountry != "country":
                    existsCountry = False
                else:
                    existsCountry = True
                    temp_info['Country'] = qualifiers_names[v].firstChild.data.capitalize()

            while(existsHost != True):
                if auxHost != "host":
                    existsHost = False
                else:
                    existsHost = True
                    temp_info['Host'] = qualifiers_names[v].firstChild.data.capitalize()
            
            while(existsCollec != True):
                if auxCollec != "collection_date":
                    existsCollec = False
                else:
                    existsCollec = True
                    temp_info['Collection_date'] = qualifiers_names[v].firstChild.data

        if existsCountry == False:
            temp_info['Country'] = ["N/A"]
        if existsHost == False: 
            temp_info['Host'] = ["N/A"]
        if existsCollec == False:
             temp_info['Collection_date'] = ["N/A"]

        #as varias condicoes do codigo pubmed
        if general[i].getElementsByTagName('INSDReference_pubmed'):
            access = general[i].getElementsByTagName('INSDReference_pubmed')
            for code in access:
                temp_info['Pubmed accession number'].append(code.firstChild.data)
        else:
            temp_info['Pubmed accession number'] = ["N/A"]

        #pegando apenas sequencias com no minimo 200 nucleotideos
        if general[i].getElementsByTagName("INSDSeq_sequence"):
            nucleotides = general[i].getElementsByTagName("INSDSeq_sequence")[0].firstChild.data
            if len(nucleotides) >= 200:
                temp_info['Nucleotide Sequence'].append(nucleotides.upper()) #verify here later
            else:
                temp_info['Nucleotide Sequence'] = ["N/A"]

        
        dict_info['Sequence'].append(temp_info['Sequence'])
        dict_info['Locus'].append(temp_info['Locus'])
        dict_info['Length'].append(temp_info['Length'])
        dict_info['Update date'].append(temp_info['Update date'])
        dict_info['Creation date'].append(temp_info['Creation date'])
        dict_info['Pubmed accession number'].append(temp_info['Pubmed accession number'])
        dict_info['Country'].append(temp_info['Country'])
        dict_info['Host'].append(temp_info['Host']) 
        dict_info['Collection_date'].append(temp_info['Collection_date'])
        dict_info['Nucleotide Sequence'].append(temp_info['Nucleotide Sequence'])

        dict_extra['Locus'].append(temp_info['Locus'])
        dict_extra['Pubmed accession number'].append(temp_info['Pubmed accession number'])

#convertendo o dicionário em um DataFrame

dict_df = pd.DataFrame(dict_info)
extra_df = pd.DataFrame(dict_extra)
df_explode = extra_df.explode(column = 'Pubmed accession number')

#salvando o DataFrame em um arquivo CSV e excel
dict_df.to_csv('collected_data.csv', index = False)
df_explode.to_csv('pubmed_accessions.csv', index = False)
#dict_df.to_excel('collected_data.xlsx', index = False)

dados = pd.read_csv('collected_data.csv')
more = pd.read_csv('pubmed_accessions.csv')

print(dict_df) 
print("\n\nDataFrame separado com os valores de locus e o codigo de acesso do pubmed")
print(extra_df)




