from catch_offers import CatchOffers

if __name__ == '__main__':
    catchOffers = CatchOffers()

    '''testeURL, testeIMG = catchOffers.getDailyGamesOffers()
    testeOri, testeFin = catchOffers.getDailyGamesOffersPrices()

    print('URL: ' + str(testeURL))
    print('Imagem: ' + str(testeIMG))
    print('Original: ' + str(testeOri))
    print('Final: ' + str(testeFin))'''

    '''testeURL_2, testeIMG_2 = catchOffers.getSpotlightOffers()

    print('URL: ' + str(testeURL_2) + '\n')
    print('Imagem: ' + str(testeIMG_2) + '\n')'''

    print(catchOffers.getSpotlightOffersContentH2())