from bs4 import BeautifulSoup
from re import sub

def getReviewTotalAmount(soup: BeautifulSoup) -> list:
    """ Função responsável por retornar uma lista contendo a quantidade total de 
    análises de um jogo.

    Parameters
    -----------
    soup: :class:`BeautifulSoup`

    Returns
    -----------
    totalReviews: :class:`list`
    """
    
    totalReviews = []

    for reviews in soup.find('div', id='userReviews').find_all('div', class_='summary'):
        for amountReviews in reviews.find_all('span', class_='responsive_hidden'):
            temp = sub(r"\s+", "" , amountReviews.contents[0]).replace(",", ".").replace("(", "").replace(")", "")
            totalReviews.append(temp)

    return totalReviews