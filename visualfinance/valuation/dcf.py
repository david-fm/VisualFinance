from typing import List
def FCF(Nopat: float, Depreciacion: float, Amortizacion: float,
        Capex: float, VariacionCapitalTrabajo: float) -> float:
    """
    Calcula el Flujo de Caja Libre (Free Cash Flow, FCF).

    Args:
        Nopat (float): Beneficio operativo despues de impuestos (Net Operating Profit After Taxes).
        Depreciacion (float): Depreciación contable del periodo.
        Amortizacion (float): Amortización contable del periodo.
        Capex (float): Gastos de capital (inversiones en activos).
        VariacionCapitalTrabajo (float): Cambios en capital de trabajo operativo.

    Returns:
        float: FCF --> Efectivo disponible para accionistas y acreedores.
    """

    return Nopat + Depreciacion + Amortizacion - Capex - VariacionCapitalTrabajo

def NOPAT(Ebit:float,TasaImpositiva:float)->float:
    """
    Beneficio operativo despues de impuestos (Net Operating Profit After Taxes)

    Args:
        Ebit (float): Beneficio antes de intereses e impuestos (Earnings Before Interest and Taxes)
        TasaImpositiva (float): Tasa de deducciones fiscales (impuestos)

    Returns:
        float: NOPAT (Net Operating Profit After Taxes) --> Mide el rendimiento operativo real descontando impuestos, pero sin tener en cuenta la deuda
    """
    return Ebit*(1-TasaImpositiva)

def EBIT(Ingresos:float,CostosOperativos:float,GastosGenerales:float)->float:
    """
    Beneficio antes de intereses e impuestos (Earnings Before Interest and Taxes)

    Args:
        Ingresos (float): Ingresos totales de la empresa
        CostosOperativos (float): Costos operacionales de la empresa para producir sus ingresos
        GastosGenerales (float): Gastos generales que no necesariamente son operativos (Excluye intereses e impuestos)

    Returns:
        float: Evalúa la rentabilidad operativa pura, sin considerar la deuda ni los impuestos
    """
    return Ingresos-(CostosOperativos+GastosGenerales)

def EBITDA(Ebit:float,Depreciacion:float,Amortizacion:float)->float:
    """Beneficio antes de intereses, impuestos, depreciaciones y amortizaciones.

    Args:
        Ebit (float): Beneficio antes de intereses e impuestos (Earnings Before Interest and Taxes)
        Depreciacion (float): Asignación contable que refleja la pérdida de valor de activos físicos (como maquinaria) por uso o tiempo
        Amortizacion (float): Similar a la depreciación, pero para activos intangibles (como licencias o software)

    Returns:
        float: Mide la rentabilidad operativa antes de impactos contables y financieros. Ideal para comparar empresas con diferentes estructuras financieras
    """
    return Ebit+Depreciacion+Amortizacion


def calculate_dcf_present_value(
    discount_rate: float,
    free_cash_flows: List[float],
    terminal_value: float
) -> float:
    """
    Calcula el Valor Presente (VP) de una serie de flujos de caja futuros y un
    valor terminal, descontados a una tasa específica.

    Args:
        discount_rate (float): La tasa de descuento a utilizar para traer los
            flujos futuros a valor presente. Normalmente es el WACC o el Coste
            de Capital (Ke).
        free_cash_flows (List[float]): Una lista con los Flujos de Caja Libres
            (FCF) proyectados para los próximos N años.
            **Este es un parámetro basado en hipótesis y análisis humano.**
        terminal_value (float): La estimación del valor de la empresa al final
            del período de proyección (año N).
            **Este es un parámetro basado en hipótesis y análisis humano.**

    Returns:
        float: El valor presente total de la empresa (Enterprise Value si se
               usan FCFF y WACC).
    """
    present_value = 0.0

    # 1. Descontar cada flujo de caja libre del período de proyección explícito
    for i, fcf in enumerate(free_cash_flows):
        period = i + 1
        present_value += fcf / ((1 + discount_rate) ** period)

    # 2. Descontar el valor terminal
    #    Se descuenta por el número de períodos en la proyección explícita.
    num_periods = len(free_cash_flows)
    present_value_terminal = terminal_value / \
        ((1 + discount_rate) ** num_periods)

    # 3. Sumar ambos componentes
    total_present_value = present_value + present_value_terminal

    return total_present_value

