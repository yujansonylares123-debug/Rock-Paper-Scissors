# RPS.py

# Función auxiliar: movimiento que gana al dado
def counter_move(move):
    if move == "R":
        return "P"  # Papel gana a Piedra
    if move == "P":
        return "S"  # Tijera gana a Papel
    if move == "S":
        return "R"  # Piedra gana a Tijera
    # Por seguridad
    return "R"

# Función auxiliar: devuelve True si m1 gana a m2
def beats(m1, m2):
    return (
        (m1 == "R" and m2 == "S") or
        (m1 == "P" and m2 == "R") or
        (m1 == "S" and m2 == "P")
    )

# Predice la próxima jugada a partir de un historial
# usando patrones (n-grams) de longitud hasta max_len
def predict_from_history(history, max_len=3):
    if not history:
        # Sin información, asumimos R para empezar
        return "R"

    counts = {"R": 0, "P": 0, "S": 0}
    hist = history
    max_len = min(max_len, len(hist))

    # Para cada longitud de patrón desde 1 hasta max_len
    for l in range(1, max_len + 1):
        pattern = hist[-l:]  # patrón: últimos l movimientos
        # Recorremos el historial buscando ese patrón
        for i in range(len(hist) - l):
            if hist[i:i + l] == pattern:
                next_move = hist[i + l]
                counts[next_move] += 1

    # Si no se encontró ningún patrón repetido,
    # usamos frecuencias globales de todo el historial
    if counts["R"] == counts["P"] == counts["S"] == 0:
        for m in hist:
            counts[m] += 1

    # Devolvemos la jugada más probable según los conteos
    predicted = max(counts, key=counts.get)
    return predicted


def player(
    prev_play,
    opponent_history=[],
    player_history=[],
    strategy_scores=[0, 0],     # [score_estrategia_A, score_estrategia_B]
    last_guesses=[None, None]   # [último_mov_EA, último_mov_EB]
):
    # Actualizar historial y puntajes con el resultado de la ronda anterior
    if prev_play != "":
        opponent_history.append(prev_play)

        # Actualizamos puntaje de cada estrategia
        for i in range(2):
            g = last_guesses[i]
            if g is None:
                continue
            if g == prev_play:
                # Empate: no sumamos ni restamos
                continue
            if beats(g, prev_play):
                strategy_scores[i] += 1
            else:
                strategy_scores[i] -= 1

    # --- Estrategia A: predecir directamente al oponente ---
    predicted_opp = predict_from_history(opponent_history)
    guess_A = counter_move(predicted_opp)

    # --- Estrategia B: suponer que el bot intenta predecirnos a nosotros ---
    # 1) Predecimos qué jugada cree el bot que haremos nosotros
    predicted_self = predict_from_history(player_history)
    # 2) Si el bot intenta ganarnos, jugaría el counter de nuestra jugada prevista
    bot_expected_move = counter_move(predicted_self)
    # 3) Nosotros jugamos el counter de lo que creemos que hará el bot
    guess_B = counter_move(bot_expected_move)

    # Elegir la mejor estrategia según puntajes acumulados
    # Si van igual, preferimos la A por defecto
    best_idx = 0 if strategy_scores[0] >= strategy_scores[1] else 1
    guess = guess_A if best_idx == 0 else guess_B

    # Primer movimiento (sin historial del rival): algo fijo y simple
    if prev_play == "":
        guess = "R"

    # Guardamos las jugadas que habría hecho cada estrategia
    last_guesses[0] = guess_A
    last_guesses[1] = guess_B

    # Guardamos nuestra jugada real en el historial propio
    player_history.append(guess)

    return guess
# Fin de RPS.py