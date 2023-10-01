from urllib.parse import urlparse, urlunparse
from lxml import etree


def extract_unique_domains(response_content: str) -> set[str]:
    """
    Extract list of unique urls from html response content
    """

    hrefs_xpath = ".//*[@href]/@href"
    html_tree = etree.HTML(response_content)
    link_elements = html_tree.xpath(hrefs_xpath)
    links_raw = [str(element) for element in link_elements]
    domains = []
    for link in links_raw:
        domain = clean_url(link)
        if domain:
            domains.append(domain)
    return set(domains)


def clean_url(url: str) -> str:
    """
    Extract the domain from url
    """
    parse_result = urlparse(url)
    if parse_result.netloc:
        domain = urlunparse([parse_result.scheme, parse_result.netloc] + [""] * 4)
        return domain
    return ""


def is_bad_domain(response_content: str) -> bool:
    """
    Recognize is domain is hacker, darkweb etc

    """
    return True
