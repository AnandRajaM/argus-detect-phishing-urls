from urllib.parse import urlparse
import sitesniffer
from datetime import datetime 
import requests
import whois


def calculate_uti(url):

    confidence_score = 0

    try:
        ssl_info = sitesniffer.get_ssl_info(url)

        #Cheching Validity Period  #1
        
        current_date = datetime.utcnow()
        not_before = datetime.strptime(ssl_info['notBefore'], '%b %d %H:%M:%S %Y %Z')
        not_after = datetime.strptime(ssl_info['notAfter'], '%b %d %H:%M:%S %Y %Z')
        if not_before <= current_date <= not_after:
            confidence_score += 0.2
        
        recognized_issuers = ['Amazon', 'Comodo', 'DigiCert', 'Symantec', 'GlobalSign', 'Let\'s Encrypt', 'GoDaddy', 'Entrust', 'Thawte', 'GeoTrust', 'RapidSSL', 'Trustwave', 'Network Solutions', 'Namecheap', 'SSL.com', 'Buypass', 'Sectigo', 'IdenTrust', 'TrustCor', 'QuoVadis', 'Actalis', 'Certum', 'WISeKey', 'SwissSign', 'StartCom', 'WoSign', 'Certum', 'TWCA', 'SecureTrust', 'USERTrust', 'Sectigo', 'AC Camerfirma', 'TrustAsia', 'Trustico', 'GMO GlobalSign', 'Global Chambersign', 'SwissSign', 'E-Tugra', 'Cambridge University', 'Telia', 'Microsec', 'Certigna', 'GlobalSign', 'AffirmTrust', 'MSCTrustgate', 'Buypass', 'Dhimyotis', 'Certigna', 'WISeKey', 'CA Disig', 'T-Systems', 'ACCV', 'Trustis', 'CAcert', 'Dhimyotis', 'Camerfirma', 'OpenTrust', 'Hongkong Post', 'Ceska Posta', 'Microsec', 'Swisscom', 'ETSI', 'Camerfirma', 'Disig', 'GlobalSign', 'Asseco', 'Certum', 'Camerfirma', 'GlobalSign', 'LuxTrust', 'PKIoverheid', 'Swisscom', 'Certigna', 'ACCV', 'S-Innovations', 'GeoTrust', 'TeliaSonera', 'Verizon', 'T-Systems', 'Izenpe', 'Agencia Notarial', 'AC Camerfirma', 'Trustwave', 'Certum', 'WISeKey', 'Camerfirma', 'SecureTrust', 'GDCA', 'Let\'s Encrypt', 'Buypass', 'AC Camerfirma', 'Certum', 'Certinomis', 'WISeKey', 'Serasa', 'Unizeto', 'CNNIC', 'GlobalSign', 'TurkTrust', 'OpenTrust', 'RSA Security', 'Certum', 'SZAFIR', 'ACT', 'Certum', 'SwissSign', 'WISeKey', 'Camerfirma', 'TWCA', 'Camerfirma', 'GlobalSign', 'SK ID Solutions', 'GlobalSign', 'DocuSign', 'Trustwave', 'GlobalSign', 'AffirmTrust', 'WISeKey', 'DigiCert', 'GoDaddy', 'Amazon', 'Entrust', 'Comodo', 'GlobalSign', 'RapidSSL', 'Thawte', 'GeoTrust', 'Symantec', 'Let\'s Encrypt', 'Trustwave', 'IdenTrust', 'Sectigo', 'Network Solutions', 'Namecheap', 'SSL.com', 'Buypass', 'Actalis', 'Certum', 'QuoVadis', 'Sectigo', 'TrustCor', 'Entrust', 'Certigna', 'WISeKey', 'SwissSign', 'StartCom', 'TrustAsia', 'USERTrust', 'AC Camerfirma', 'GMO GlobalSign', 'Global Chambersign', 'SecureTrust', 'AffirmTrust', 'MSCTrustgate', 'Buypass', 'Dhimyotis', 'E-Tugra', 'Camerfirma', 'GlobalSign', 'Microsec', 'Trustico', 'Certigna', 'TWCA', 'Hongkong Post', 'T-Systems', 'Camerfirma', 'Trustis', 'CAcert', 'Disig', 'Ceska Posta', 'Swisscom', 'ETSI', 'Certum', 'GlobalSign', 'Asseco', 'LuxTrust', 'PKIoverheid', 'ACCV', 'S-Innovations', 'Verizon', 'TeliaSonera', 'GeoTrust', 'Agencia Notarial', 'Izenpe', 'Certinomis', 'Serasa', 'Unizeto', 'CNNIC', 'OpenTrust', 'RSA Security', 'SZAFIR', 'ACT', 'SK ID Solutions', 'DocuSign', 'Trustwave']

        #Checking the Issuer #2
        try:
            issuer = ssl_info['issuer'][0][0][1]
            if issuer in recognized_issuers:
                confidence_score += 0.2
        except Exception as e:
            print(e)
            pass
        
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        # Check subject based on URL #3
        try:
            subject = ssl_info['subject'][0][0][1]
            if domain in subject:
                confidence_score += 0.2
        except Exception as e:
            print(e)
            pass
    
        try:
            # Check subject alternative names (SANs) #4
            san_domains = [san[1] for san in ssl_info['subjectAltName']]
            if domain in san_domains:
                confidence_score += 0.2
        except Exception as e:
            print(e)
            pass
        
        # Check OCSP and CRL #4
        try:
            if ssl_info.get('OCSP') and ssl_info.get('crlDistributionPoints'):
                confidence_score += 0.2
        except Exception as e:
            print(e)
            pass

    except Exception as e:
        print(e)
        confidence_score -= 2
    
        
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    # Check OpenPage Rank score #5
    base_url = 'https://openpagerank.com/api/v1.0/'
    endpoint = 'getPageRank'
    url = base_url + endpoint
    params = {'domains[]': domain}
    headers = {'API-OPR': 'cw8w8gc4048s08sskc40gos80004040kcwkkkswc'}
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            response = data.get('response')

            if response:
                for result in response:
                    if result['status_code'] == 200:
                        if result['page_rank_decimal'] > 4:
                            confidence_score += 0.2
                    else:
                        print(f"Error: {result['error']}")
            else:
                print("Failed to fetch PageRanks.")
        else:
            print("Error:", response.status_code, response.text)
            
    except Exception as e:
        print("Error:", str(e))
        pass
        

    # Check if the domain is older than 200 days #6
    current_date = datetime.utcnow()
    domain_info = whois.whois(domain)
    try:
        creation_date = domain_info.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if creation_date:
            if (current_date - creation_date).days > 200:
                confidence_score += 0.2
        
    except whois.parser.PywhoisError as e:
        print("Error:", e)
        pass
    
    #checking if the domain has a valid HTTPS certificate #7
    try:
        response = requests.get(f"https://{domain}")
        if response.status_code == 200  :
            confidence_score += 0.2
        
    except requests.RequestException as e:
        print("Error:", e)
        pass
        

    return round((confidence_score/1.4) *9 + 1 , 2)


