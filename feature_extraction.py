import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import string





def extract_parameters(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            
            print(url)
            # Extract URL parameters
            urllength = len(url)
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            domain_length = len(domain)
            tld = domain.split('.')[-1] 
            tld_length = len(tld)
            no_of_subdomain = len(parsed_url.hostname.split('.')) - 2  # Subtracting 2 for removing domain and TLD
            url = url.replace("https://", "")
            url = url.replace("www.", "")
            no_of_letters_in_url = sum(url.count(char) for char in string.ascii_letters)
            letter_ratio_in_url = sum(c.isalpha() for c in url) / len(url)
            no_of_digits_in_url = sum(url.count(char) for char in string.digits)
            digit_ratio_in_url = no_of_digits_in_url / len(url)
            no_of_equals_in_url = url.count('=')
            no_of_qmark_in_url = url.count('?')
            no_of_ampersand_in_url = url.count('&')
            no_of_other_special_chars_in_url = len(url) - (no_of_letters_in_url + no_of_digits_in_url + no_of_equals_in_url + no_of_qmark_in_url + no_of_ampersand_in_url)
            spacial_char_ratio_in_url = no_of_other_special_chars_in_url / len(url)
            is_https = parsed_url.scheme == 'https'
            
            # Extract HTML content parameters
            has_title = 1 if soup.title else 0
            title = soup.title.text if soup.title else None
            has_favicon = 1 if soup.find('link', rel='icon') else 0
            has_description = 1 if soup.find('meta', attrs={'name': 'description'}) else 0
            no_of_popup = len(soup.find_all('div', class_='popup'))  # Example, you need to adjust according to your HTML structure
            no_of_iframe = len(soup.find_all('iframe'))
            has_external_form_submit = 1 if soup.find('form', attrs={'target': '_blank'}) else 0
            has_submit_button = 1 if soup.find('input', type='submit') else 0
            has_hidden_fields = 1 if soup.find('input', type='hidden') else 0
            has_password_field = 1 if soup.find('input', type='password') else 0
            robots = 1 if soup.find('meta', attrs={'name': 'robots'}) else 0
            no_of_image = len(soup.find_all('img'))
            no_of_css = len(soup.find_all('link', rel='stylesheet'))
            no_of_js = len(soup.find_all('script'))
            
             
            # Return the extracted parameters as a dictionary
            return {
                
                'URLLength': urllength,
                'DomainLength': domain_length,
                'TLDLength': tld_length,
                'NoOfSubDomain': no_of_subdomain,
                'NoOfLettersInURL': no_of_letters_in_url,
                'LetterRatioInURL': letter_ratio_in_url,
                'NoOfDegitsInURL': no_of_digits_in_url,
                'DegitRatioInURL': digit_ratio_in_url,
                'NoOfEqualsInURL': no_of_equals_in_url,
                'NoOfQMarkInURL': no_of_qmark_in_url,
                'NoOfAmpersandInURL': no_of_ampersand_in_url,
                'NoOfOtherSpecialCharsInURL': no_of_other_special_chars_in_url,
                'SpacialCharRatioInURL': spacial_char_ratio_in_url,
                'IsHTTPS': is_https,
                'HasTitle': has_title,
                'HasFavicon': has_favicon,
                'Robots': robots,
                'HasDescription': has_description,
                'NoOfPopup': no_of_popup,
                'NoOfiFrame': no_of_iframe,
                'HasExternalFormSubmit': has_external_form_submit,
                'HasSubmitButton': has_submit_button,
                'HasHiddenFields': has_hidden_fields,
                'HasPasswordField': has_password_field,
                'NoOfImage': no_of_image,
                'NoOfCSS': no_of_css,
                'NoOfJS': no_of_js
            }
        else:
            print("Error: Unable to fetch URL, status code:", response.status_code)
            return None
    except Exception as e:
        print("Error:", e)
        return None
