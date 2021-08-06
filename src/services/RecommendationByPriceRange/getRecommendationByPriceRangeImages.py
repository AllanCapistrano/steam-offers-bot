from bs4 import BeautifulSoup

def getRecommendationByPriceRangeImages(soup: BeautifulSoup) -> list:
        """ Função responsável por retornar uma lista contendo as imagens dos 
        jogos que estão na faixa de preço especificada.

        Parameters
        -----------
        soup: :class:`BeautifulSoup`

        Returns
        -----------
        images: :class:`list`
        """
        
        images = []

        for listDivGamesImages in soup.find_all('div', class_="search_capsule"):
            for listImgGamesImages in listDivGamesImages.find_all('img'):
                img = listImgGamesImages.attrs['srcset'].split(" ")[2]
                images.append(img)

        return images