# Removendo acentuação e caracteres especiais.
from unidecode import unidecode

def genreFormatting(unformattedGenre : str) -> str:
    """Função responsável pela formatação do gênero do jogo.

    Parameters
    -----------
    unformattedGenre: :class:`str`
        Gênero do jogo.

    Returns
    -----------
    genre: :class:`str`
        Gênero do jogo formatado.
    """
    
    # Removendo acentuação e caracteres especiais.
    genre = unidecode(unformattedGenre)
    # Convertendo o gênero para lower case.
    genre = genre.lower()

    # ------------------------------ Action ------------------------------ #
    if(genre == 'acao'):
        genre = 'action'
    elif(genre == 'arcade e ritmo' or genre == 'arcade' or genre == 'ritmo'):
        genre = 'arcade_rhythm'
    elif(genre == 'luta e artes marciais' or genre == 'luta' or genre == 'artes marciais'):
        genre = 'fighting_martial_arts'
    elif(
        genre == 'plataformas e corridas interminaveis' or
        genre == 'plataformas' or
        genre == 'plataforma' or
        genre == 'corridas interminaveis'
    ):
        genre = 'action_run_jump'
    elif(genre == 'porradaria'):
        genre = 'action_beat_em_up'
    elif(genre == 'roguelike de acao'):
        genre = 'action_rogue_like'
    elif(genre == 'tiro em terceira pessoa' or genre == 'tps'):
        genre = 'action_tps'
    elif(genre == 'tiro em primeira pessoa' or genre == 'fps'):
        genre = 'action_fps'
    # ----------------------- Adventure and Casual ----------------------- #
    elif(genre == 'aventura e casual'):
        genre = 'adventure_and_casual'
    elif(genre == 'aventura'):
        genre = 'adventure'
    elif(genre == 'casuais'):
        genre = 'casual'
    elif(
        genre == 'quebra-cabeca' or 
        genre == 'puzzle' or 
        genre == 'puzzles'
    ):
        genre = 'puzzle_matching'
    elif(genre == 'rpg de aventura' or genre == 'rpgs de aventura'):
        genre = 'adventure_rpg'
    elif(genre == 'romance visual' or genre == 'visual novel'):
        genre = 'visual_novel'
    elif(genre == 'trama excepcional'):
        genre = 'interactive_fiction'
    # ---------------------------- RPG ----------------------------------- #
    elif(genre == 'rpg de acao' or genre == 'rpgs de acao'):
        genre = 'rpg_action'
    elif(genre == 'jrpg'):
        genre = 'rpg_jrpg'
    elif(
        genre == 'rpg de estrategia' or
        genre == 'rpgs de estrategia' or
        genre == 'rpg de tatica e estrategia' or 
        genre == 'rpg de tatica'
    ):
        genre = 'rpg_strategy_tactics'
    elif(
        genre == 'rpg de grupos' or 
        genre == 'rpg de grupo' or
        genre == 'rpg em grupos' or 
        genre == 'rpg em grupo' or
        genre == 'rpgs em grupo'
    ):
        genre = 'rpg_party_based'
    elif(
        genre == 'rpgs em turnos' or 
        genre == 'rpg em turnos' or 
        genre == 'rpg em turno' or
        genre == 'rpg de turnos' or 
        genre == 'rpg de turno'
    ):
        genre = 'rpg_turn_based'
    elif(
        genre == 'roguelikes e roguelites' or 
        genre == 'roguelikes' or
        genre == 'roguelike' or
        genre == 'roguelites' or
        genre == 'roguelite'
    ):
        genre = 'rogue_like_rogue_lite'
    # ------------------------- Simulation ------------------------------- #
    elif(genre == 'simulacao' or genre == 'simulador'):
        genre = 'simulation'
    elif(
        genre == 'construcao e automacao' or 
        genre == 'construcao' or 
        genre == 'automacao'
    ):
        genre = 'sim_building_automation'
    elif(genre == 'encontros' or genre == 'encontro'):
        genre = 'sim_dating'
    elif(
        genre == 'espaco e aviacao' or 
        genre == 'espaco' or 
        genre == 'aviacao'
    ):
        genre = 'sim_space_flight'
    elif(
        genre == 'fisica e faca o que quiser' or 
        genre == 'fisica' or
        genre == 'sandbox'
    ):
        genre = 'sim_physics_sandbox'
    elif(genre == 'gestao de negocios' or genre == 'negocios'):
        genre = 'sim_business_tycoon'
    elif(
        genre == 'rurais e de fabricacao' or 
        genre == 'rurais' or 
        genre == 'fabricacao'
    ):
        genre = 'sim_farming_crafting'
    elif(
        genre == 'vida e imersivos' or 
        genre == 'vida' or 
        genre == 'imersivos'
    ):
        genre = 'sim_life'
    # --------------------------- Strategy ------------------------------- #
    elif(genre == 'estrategia'):
        genre = 'strategy'
    elif(
        genre == 'cidades e colonias' or
        genre == 'cidades' or
        genre == 'cidade' or
        genre == 'colonias' or
        genre == 'colonia'
    ):
        genre = 'strategy_cities_settlements'
    elif(genre == 'defesa de torres' or genre == 'tower defense'):
        genre = 'tower_defense'
    elif(
        genre == 'estrategia baseada em turnos' or 
        genre == 'estrategia em turnos'
    ):
        genre = 'strategy_turn_based'
    elif(genre == 'estrategia em tempo real' or genre == 'rts'):
        genre = 'strategy_real_time'
    elif(
        genre == 'grande estrategia e 4x' or
        genre == 'grande estrategia' or
        genre == '4x'
    ):
        genre = 'strategy_grand_4x'
    elif(genre == 'estrategia militar' or genre == 'militar'):
        genre = 'strategy_military'
    elif(
        genre == 'tabuleiro e cartas' or
        genre == 'tabuleiro e de cartas' or
        genre == 'tabuleiro' or
        genre == 'cartas' or
        genre == 'carta'
    ):
        genre = 'strategy_card_board'
    # ---------------------- Sports and Racing --------------------------- #
    elif(genre == 'esporte e corrida'):
        genre = 'sports_and_racing'
    elif(genre == 'corrida' or genre == 'corridas'):
        genre = 'racing'
    elif(genre == 'esporte em equipe' or genre == 'esportes em equipe'):
        genre = 'sports_team'
    elif(genre == 'esportes' or genre == 'esporte'):
        genre = 'sports'
    elif(genre == 'esportes individuais' or genre == 'esporte individual'):
        genre = 'sports_individual'
    elif(
        genre == 'pescaria e caca' or 
        genre == 'pescaria' or 
        genre == 'caca'
    ):
        genre = 'sports_fishing_hunting'
    elif(
        genre == 'simulador de esportes' or 
        genre == 'simulador de esporte'
    ):
        genre = 'sports_sim'
    elif(
        genre == 'simulacao de corrida' or 
        genre == 'simulador de corrida'
    ):
        genre = 'racing_sim'

    return genre