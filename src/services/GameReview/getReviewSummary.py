from bs4 import BeautifulSoup

def getReviewSummary(soup: BeautifulSoup) -> list:
    """ Função responsável por retornar uma lista contendo o resumo das análises
    de um jogo.

    Parameters
    -----------
    soup: :class:`BeautifulSoup`

    Returns
    -----------
    summary: :class:`list`
    """
    
    summary = []

    for reviews in soup.find('div', id='userReviews').find_all('div', class_='summary'):
        for content in reviews.find_all('span', class_='game_review_summary'):
            summary.append(content.contents[0])
            

    return summary