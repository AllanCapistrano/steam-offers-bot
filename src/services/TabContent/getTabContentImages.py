from bs4 import BeautifulSoup

def getTabContentImages(soup: BeautifulSoup) -> list:
        """ Função responsável por retornar uma lista contendo as imagens dos
        jogos que estão em uma aba específica.

        Parameters
        -----------
        soup: :class:`BeautifulSoup`

        Returns
        -----------
        images: :class:`list`
        """
        
        images = []

        for tabContent in soup.find_all('img', class_='tab_item_cap_img'):
            # Alterando a resolução da imagem.
            imgResized = tabContent.attrs['src'].replace("184x69", "231x87")

            images.append(imgResized)

        return images