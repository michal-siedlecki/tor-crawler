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
        parse_result = urlparse(link)
        if parse_result.netloc and parse_result.netloc not in domains:
            domain = urlunparse([parse_result.scheme, parse_result.netloc] + [""] * 4)
            domains.append(domain)
    return set(domains)
