"""
State Name Standardization for UIDAI Data
==========================================
Maps all variant state names to official standardized versions.
"""

# Official state name mapping
STATE_NAME_MAP = {
    # Andhra Pradesh variants
    'andhra pradesh': 'Andhra Pradesh',
    'ANDHRA PRADESH': 'Andhra Pradesh',
    'Andhra pradesh': 'Andhra Pradesh',
    
    # Arunachal Pradesh variants
    'arunachal pradesh': 'Arunachal Pradesh',
    'ARUNACHAL PRADESH': 'Arunachal Pradesh',
    
    # Assam variants
    'assam': 'Assam',
    'ASSAM': 'Assam',
    
    # Bihar variants
    'bihar': 'Bihar',
    'BIHAR': 'Bihar',
    
    # Chhattisgarh variants
    'chhattisgarh': 'Chhattisgarh',
    'CHHATTISGARH': 'Chhattisgarh',
    'Chattisgarh': 'Chhattisgarh',
    
    # Delhi variants
    'delhi': 'Delhi',
    'DELHI': 'Delhi',
    'NCT of Delhi': 'Delhi',
    'NCT OF DELHI': 'Delhi',
    
    # Goa variants
    'goa': 'Goa',
    'GOA': 'Goa',
    
    # Gujarat variants
    'gujarat': 'Gujarat',
    'GUJARAT': 'Gujarat',
    
    # Haryana variants
    'haryana': 'Haryana',
    'HARYANA': 'Haryana',
    
    # Himachal Pradesh variants
    'himachal pradesh': 'Himachal Pradesh',
    'HIMACHAL PRADESH': 'Himachal Pradesh',
    
    # Jharkhand variants
    'jharkhand': 'Jharkhand',
    'JHARKHAND': 'Jharkhand',
    
    # Karnataka variants
    'karnataka': 'Karnataka',
    'KARNATAKA': 'Karnataka',
    
    # Kerala variants
    'kerala': 'Kerala',
    'KERALA': 'Kerala',
    
    # Madhya Pradesh variants
    'madhya pradesh': 'Madhya Pradesh',
    'MADHYA PRADESH': 'Madhya Pradesh',
    
    # Maharashtra variants
    'maharashtra': 'Maharashtra',
    'MAHARASHTRA': 'Maharashtra',
    
    # Manipur variants
    'manipur': 'Manipur',
    'MANIPUR': 'Manipur',
    
    # Meghalaya variants
    'meghalaya': 'Meghalaya',
    'MEGHALAYA': 'Meghalaya',
    
    # Mizoram variants
    'mizoram': 'Mizoram',
    'MIZORAM': 'Mizoram',
    
    # Nagaland variants
    'nagaland': 'Nagaland',
    'NAGALAND': 'Nagaland',
    
    # Odisha variants
    'odisha': 'Odisha',
    'ODISHA': 'Odisha',
    'Orissa': 'Odisha',
    'ORISSA': 'Odisha',
    'orissa': 'Odisha',
    
    # Punjab variants
    'punjab': 'Punjab',
    'PUNJAB': 'Punjab',
    
    # Rajasthan variants
    'rajasthan': 'Rajasthan',
    'RAJASTHAN': 'Rajasthan',
    
    # Sikkim variants
    'sikkim': 'Sikkim',
    'SIKKIM': 'Sikkim',
    
    # Tamil Nadu variants
    'tamil nadu': 'Tamil Nadu',
    'TAMIL NADU': 'Tamil Nadu',
    'Tamilnadu': 'Tamil Nadu',
    
    # Telangana variants
    'telangana': 'Telangana',
    'TELANGANA': 'Telangana',
    
    # Tripura variants
    'tripura': 'Tripura',
    'TRIPURA': 'Tripura',
    
    # Uttar Pradesh variants
    'uttar pradesh': 'Uttar Pradesh',
    'UTTAR PRADESH': 'Uttar Pradesh',
    
    # Uttarakhand variants
    'uttarakhand': 'Uttarakhand',
    'UTTARAKHAND': 'Uttarakhand',
    'Uttaranchal': 'Uttarakhand',
    
    # West Bengal variants
    'west bengal': 'West Bengal',
    'WEST BENGAL': 'West Bengal',
    'WESTBENGAL': 'West Bengal',
    'Westbengal': 'West Bengal',
    'West Bangal': 'West Bengal',
    'West bengal': 'West Bengal',
    'West  Bengal': 'West Bengal',
    
    # Andaman and Nicobar Islands variants
    'andaman and nicobar islands': 'Andaman And Nicobar Islands',
    'ANDAMAN AND NICOBAR ISLANDS': 'Andaman And Nicobar Islands',
    'Andaman & Nicobar Islands': 'Andaman And Nicobar Islands',
    'Andaman and Nicobar': 'Andaman And Nicobar Islands',
    'A & N Islands': 'Andaman And Nicobar Islands',
    
    # Chandigarh variants
    'chandigarh': 'Chandigarh',
    'CHANDIGARH': 'Chandigarh',
    
    # Dadra and Nagar Haveli and Daman and Diu variants
    'dadra and nagar haveli and daman and diu': 'Dadra And Nagar Haveli And Daman And Diu',
    'DADRA AND NAGAR HAVELI AND DAMAN AND DIU': 'Dadra And Nagar Haveli And Daman And Diu',
    'Dadra & Nagar Haveli And Daman & Diu': 'Dadra And Nagar Haveli And Daman And Diu',
    'The Dadra And Nagar Haveli And Daman And Diu': 'Dadra And Nagar Haveli And Daman And Diu',
    'Dadra and Nagar Haveli': 'Dadra And Nagar Haveli And Daman And Diu',
    'Dadra & Nagar Haveli': 'Dadra And Nagar Haveli And Daman And Diu',
    'Daman and Diu': 'Dadra And Nagar Haveli And Daman And Diu',
    'Daman & Diu': 'Dadra And Nagar Haveli And Daman And Diu',
    'DAMAN AND DIU': 'Dadra And Nagar Haveli And Daman And Diu',
    
    # Jammu and Kashmir variants
    'jammu and kashmir': 'Jammu And Kashmir',
    'JAMMU AND KASHMIR': 'Jammu And Kashmir',
    'Jammu & Kashmir': 'Jammu And Kashmir',
    'J&K': 'Jammu And Kashmir',
    'Jammu And Kashmir': 'Jammu And Kashmir',
    
    # Ladakh variants
    'ladakh': 'Ladakh',
    'LADAKH': 'Ladakh',
    
    # Lakshadweep variants
    'lakshadweep': 'Lakshadweep',
    'LAKSHADWEEP': 'Lakshadweep',
    
    # Puducherry variants
    'puducherry': 'Puducherry',
    'PUDUCHERRY': 'Puducherry',
    'Pondicherry': 'Puducherry',
    'PONDICHERRY': 'Puducherry',
}


def standardize_state_name(state_name):
    """
    Standardize a state name to official version.
    
    Parameters
    ----------
    state_name : str
        Raw state name from data
        
    Returns
    -------
    str
        Standardized state name
    """
    if not isinstance(state_name, str):
        return state_name
    
    # Strip whitespace
    cleaned = state_name.strip()
    
    # Check direct match first
    if cleaned in STATE_NAME_MAP:
        return STATE_NAME_MAP[cleaned]
    
    # Check title case
    if cleaned.title() in STATE_NAME_MAP:
        return STATE_NAME_MAP[cleaned.title()]
    
    # If no match found, return title-cased version
    return cleaned.title()


def standardize_dataframe_states(df, column='state'):
    """
    Standardize all state names in a DataFrame.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with state column
    column : str
        Name of state column
        
    Returns
    -------
    pd.DataFrame
        DataFrame with standardized state names
    """
    df = df.copy()
    df[column] = df[column].apply(standardize_state_name)
    return df
