import pandas as pd
from scipy.optimize import newton
from typing import List, Dict, Any

# Asumimos que la función para calcular el valor presente del DCF está en valuation.dcf
# La crearemos en el siguiente bloque de código.
from valuation.dcf import calculate_dcf_present_value


def calculate_implied_irr(
    current_market_price: float,
    free_cash_flow_projections: List[float],
    terminal_value_projection: float,
    initial_guess: float = 0.10
) -> float:
    """
    Calcula la Tasa Interna de Retorno (TIR) implícita para una acción.

    Esta función encuentra la tasa de descuento que iguala el valor presente de los
    flujos de caja futuros proyectados (incluido el valor terminal) con el
    precio de mercado actual de la acción. Utiliza el método de Newton para
    encontrar la raíz de la ecuación.

    Args:
        current_market_price (float): El precio actual de la acción en el mercado.
        free_cash_flow_projections (List[float]): Una lista con las proyecciones
            de Flujo de Caja Libre (FCF) para los próximos N años.
            **Este es un parámetro basado en hipótesis y análisis humano.**
        terminal_value_projection (float): La estimación del valor de la empresa
            al final del período de proyección.
            **Este es un parámetro basado en hipótesis y análisis humano.**
        initial_guess (float, optional): Una estimación inicial para la TIR.
            Por defecto es 0.10 (10%).

    Returns:
        float: La Tasa Interna de Retorno (TIR) implícita como un valor decimal.
               Retorna float('nan') si el solver no converge.
    """
    # La función objetivo que queremos que sea cero:
    # NPV(rate) - MarketPrice = 0
    def objective_function(rate): return calculate_dcf_present_value(
        discount_rate=rate,
        free_cash_flows=free_cash_flow_projections,
        terminal_value=terminal_value_projection
    ) - current_market_price

    try:
        # Usamos un solver numérico para encontrar la tasa (la raíz de la función)
        implied_rate = newton(objective_function, initial_guess)
        return implied_rate
    except (RuntimeError, OverflowError):
        # Si el solver no puede encontrar una solución, retorna NaN
        return float('nan')


def dcf_expected_returns(
    investment_universe_data: Dict[str, Dict[str, Any]]
) -> pd.Series:
    """
    Genera una serie de retornos esperados (mean_returns) para un universo de
    acciones, basándose en la TIR implícita de sus modelos DCF.

    Args:
        investment_universe_data (Dict[str, Dict[str, Any]]): Un diccionario
            donde cada clave es el ticker de una acción. El valor es otro
            diccionario que debe contener:
            - 'market_price': El precio de mercado actual.
            - 'fcf_projections': Una lista de flujos de caja proyectados.
            - 'terminal_value': El valor terminal proyectado.
            Ejemplo:
            {
                'STOCK_A': {
                    'market_price': 150.0,
                    'fcf_projections': [10, 12, 14, 15],
                    'terminal_value': 200
                },
                'STOCK_B': { ... }
            }

    Returns:
        pd.Series: Una serie de pandas donde el índice son los tickers de las
                   acciones y los valores son sus retornos esperados (TIR implícita).
    """
    expected_returns = {}
    for ticker, data in investment_universe_data.items():
        print(f"Calculando TIR implícita para {ticker}...")
        try:
            irr = calculate_implied_irr(
                current_market_price=data['market_price'],
                free_cash_flow_projections=data['fcf_projections'],
                terminal_value_projection=data['terminal_value']
            )
            expected_returns[ticker] = irr
        except KeyError as e:
            print(
                f"Error: Falta la clave {e} para el ticker {ticker}. Se omitirá.")
            expected_returns[ticker] = float('nan')

    return pd.Series(expected_returns, name="dcf_expected_returns").dropna()
