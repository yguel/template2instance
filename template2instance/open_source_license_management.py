from bs4 import BeautifulSoup
import requests
from typeguard import typechecked


known_licenses = {
    "open source":
    ["Apache-2.0","BSL-1.0","BSD-2-Clause","BSD-3-Clause","GPL-3.0","LGPL-3.0","MIT","MIT-0"]
}

python_short_text = """
# This file is licensed under the %(LICENCE_NAME)s License.
# You may obtain a copy of the License at %(LICENCE_URL)s
"""

@typechecked
def get_license_text(license : str) -> str:
    """
    This function returns the text of an open source license from the 
    OSI website.

    Parameters
    ----------
    license : str
        The license name that should match one of the names in known_licenses
    
    Returns
    -------
    str
        The text of the license

    Raises
    ------
    Exception
        If the license is not found at the OSI 
        website with url https://opensource.org/licenses/<license>
    """
    url = "https://opensource.org/licenses/"+license
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    license_text = soup.find_all('div', class_='field-item even')
    return license_text[0].get_text()

@typechecked
def get_licence_url(license : str, fails_if_url_not_reachable : bool = False) -> str:
    """
    This function returns the url of an open source license from the OSI website.

    Parameters
    ----------
    license : str
        The license name that should match one of the names in known_licenses
    fails_if_url_not_reachable : bool
        If True, the function raises an exception if the url is not reachable. 
        Otherwise, it returns the url anyway.
        Default is False.

    Returns
    -------
    str
        The url of the license

    Raises
    ------
    Exception
        If the license is not found in known_licenses
        If the license is not found at the OSI website with 
        url https://opensource.org/licenses/<license> and fails_if_url_not_reachable is True
    """
    if license in known_licenses["open source"]:
        url = "https://opensource.org/licenses/"+license
        # check that the url is valid (does not return 404)
        response = requests.get(url)
        if response.status_code == 200:
            return url
        else:
            if fails_if_url_not_reachable:
                raise Exception(f"License {license} not found at {url}. Maybe it is not an open source license or there is a network issue.")
            return "https://opensource.org/licenses/"+license
    else:
        raise Exception(f"License {license} not found in known_licenses.")
    
@typechecked
def check_known_license( license : str ) -> bool:
    """
    This function checks if a license is in the list of known open source licenses.

    Parameters
    ----------
    license : str
        The license name that should match one of the names in known_licenses regardless of case

    Returns
    -------
    bool
        True if the license is in known_licenses, False otherwise
    """
    return license.lower() in [x.lower() for x in known_licenses["open source"]]

@typechecked
def get_normalized_license_name(license : str ) -> str:
    """
    This function returns the normalized name of a license from the list of known open source licenses.

    Parameters
    ----------
    license : str
        The license name that should match one of the names in known_licenses regardless of case

    Returns
    -------
    str
        The normalized name of the license
    """
    if check_known_license(license):
        return [x for x in known_licenses["open source"] if x.lower() == license.lower()][0]
    else:
        raise Exception(f"License {license} not found in known licenses {known_licenses}.")
    
@typechecked
def get_license_short_text(license : str, fails_if_url_not_reachable_for_check : bool = True ) -> str:
    """
    This function returns a short text for a licence whose text can be found online.

    Parameters
    ----------
    license : str
        The license name that should match one of the names in known_licenses
    
    fails_if_url_not_reachable_for_check : bool
        If True, the function raises an exception if the url is not reachable. 
        Otherwise, it returns the url anyway.
        Default is True.

    Returns
    -------
    str
        The short text of the license

    Raises
    ------
    Exception
        If the license is not found in known_licenses
        If the license cannot be check online and fails_if_url_not_reachable_for_check is True, 
        then an exception is raised in the call of get_licence_url.
    """

    if check_known_license(license):
        # get the correct name of the license in the table of known licenses
        true_name = get_normalized_license_name(license)
        return python_short_text % {"LICENCE_NAME":true_name,"LICENCE_URL":get_licence_url(true_name, fails_if_url_not_reachable_for_check)}
    else:
        raise Exception(f"License {license} not found in known_licenses.")