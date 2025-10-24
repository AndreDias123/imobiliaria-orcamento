from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional, List, Dict
import sys, csv

CONTRACT_FEE = 2000.00
MAX_INSTALLMENTS = 5

# --------- Modelos ---------
class Imovel(ABC):
    @abstractmethod
    def calcular_aluguel(self) -> float: ...

from dataclasses import dataclass

@dataclass
class Apartamento(Imovel):
    quartos: int = 1
    vagas: int = 0
    tem_criancas: bool = True
    def calcular_aluguel(self) -> float:
        v = 700.0
        if self.quartos == 2: v += 200.0
        if self.vagas > 0: v += 300.0
        if not self.tem_criancas: v *= 0.95
        return round(v, 2)

@dataclass
class Casa(Imovel):
    quartos: int = 1
    vagas: int = 0
    def calcular_aluguel(self) -> float:
        v = 900.0
        if self.quartos == 2: v += 250.0
        if self.vagas > 0: v += 300.0
        return round(v, 2)

@dataclass
class Estudio(Imovel):
    vagas: int = 0
    def calcular_aluguel(self) -> float:
        v = 1200.0
        if self.vagas == 0: return round(v, 2)
        if self.vagas <= 2: return round(v + 250.0, 2)
        return round(v + 250.0 + (self.vagas-2)*60.0, 2)

# --------- Serviços ---------
@dataclass
class Orcamento:
    imovel: Imovel
    parcelas_contrato: int
    def validar(self) -> None:
        if not (1 <= self.parcelas_contrato <= MAX_INSTALLMENTS):
            raise ValueError(f"Parcelas do contrato devem estar entre 1 e {MAX_INSTALLMENTS}.")
    def aluguel_mensal(self) -> float: return round(self.imovel.calcular_aluguel(), 2)
    def parcela_contrato(self) -> float: return round(CONTRACT_FEE / self.parcelas_contrato, 2)
    def total_mensal(self) -> float: return round(self.aluguel_mensal() + self.parcela_contrato(), 2)
    def gerar_parcelas_12_meses(self) -> List[Dict[str, float]]:
        aluguel = self.aluguel_mensal(); parcela = self.parcela_contrato()
        out = []
        for mes in range(1, 13):
            pc = parcela if mes <= self.parcelas_contrato else 0.0
            out.append({"mes": mes, "aluguel": aluguel, "parcela_contrato": pc, "total": round(aluguel+pc,2)})
        return out

def salvar_csv(orc: Orcamento, caminho: str, corretor: str, cliente: str) -> None:
    linhas = orc.gerar_parcelas_12_meses()
    # vamos repetir corretor e cliente em cada linha para facilitar filtros depois
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        cols = ["mes","aluguel","parcela_contrato","total","corretor","cliente"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for l in linhas:
            l["corretor"] = corretor
            l["cliente"]  = cliente
            w.writerow(l)

# --------- CLI ---------
def ler_int(msg, minimo=None, maximo=None):
    while True:
        try:
            v = int(input(msg).strip())
            if minimo is not None and v < minimo: print(f"≥ {minimo}"); continue
            if maximo is not None and v > maximo: print(f"≤ {maximo}"); continue
            return v
        except ValueError: print("Digite um número inteiro válido.")

def ler_bool(msg):
    while True:
        v = input(msg + " [s/n]: ").strip().lower()
        if v in {"s","sim"}: return True
        if v in {"n","nao","não"}: return False
        print("Responda com 's' ou 'n'.")

def main():
    print("\n=== Orçamento - CSV ===\n")
    corretor = input("Nome do corretor: ").strip() or "—"
    cliente  = input("Nome do cliente: ").strip() or "—"

    print("\nTipo de imóvel:\n  1) Apartamento\n  2) Casa\n  3) Estúdio")
    tipo = input("Escolha [1-3]: ").strip()
    if tipo == "1":
        quartos = ler_int("Número de quartos (1 ou 2): ", 1, 2)
        vagas = ler_int("Vagas de garagem (0+): ", 0, None)
        tem_criancas = ler_bool("Há crianças no domicílio?")
        imovel = Apartamento(quartos, vagas, tem_criancas)
    elif tipo == "2":
        quartos = ler_int("Número de quartos (1 ou 2): ", 1, 2)
        vagas = ler_int("Vagas de garagem (0+): ", 0, None)
        imovel = Casa(quartos, vagas)
    else:
        vagas = ler_int("Vagas de estacionamento (0+): ", 0, None)
        imovel = Estudio(vagas)

    parcelas = ler_int(f"Nº de parcelas do contrato [1..{MAX_INSTALLMENTS}]: ", 1, MAX_INSTALLMENTS)
    orc = Orcamento(imovel=imovel, parcelas_contrato=parcelas); orc.validar()

    print("\n--- Resultado ---")
    print("Aluguel mensal: R$", orc.aluguel_mensal())
    print("Parcela do contrato: R$", orc.parcela_contrato())
    print("Total mensal (com parcela): R$", orc.total_mensal())

    nome = input("\nNome do arquivo CSV (ENTER para 'parcelas_orcamento.csv'): ").strip() or "parcelas_orcamento.csv"
    salvar_csv(orc, nome, corretor, cliente)
    print("CSV salvo em:", nome)

if __name__ == "__main__":
    main()
