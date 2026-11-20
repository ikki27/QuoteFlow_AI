"""Osnovni enotski testi poslovne logike, validacij in API končnih točk."""
from decimal import Decimal as D

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.common import plain_decimal
from app.pricing import cena_postavke, izmera_skupaj, vrednost_izmere, vsote_dokumenta

client = TestClient(app)


# Poslovna logika: izmere

def test_izmera_m2_je_dolzina_krat_visina():
    assert vrednost_izmere('m2', dolzina=D('4'), visina=D('5')) == D('20')


def test_izmera_kosi_mnozijo_vrednost():
    assert vrednost_izmere('m', kosi=D('3'), dolzina=D('2.5')) == D('7.5')


def test_odsteta_izmera_zmanjsa_skupno_vrednost():
    izmere = [{'dolzina': D('10'), 'visina': D('3')}, {'dolzina': D('2'), 'visina': D('1'), 'odstej': True}]
    assert izmera_skupaj('m2', izmere) == D('28')


def test_negativna_skupna_izmera_je_zavrnjena():
    with pytest.raises(ValueError):
        izmera_skupaj('m', [{'dolzina': D('1')}, {'dolzina': D('2'), 'odstej': True}])


def test_neznana_merska_enota_je_zavrnjena():
    with pytest.raises(ValueError):
        vrednost_izmere('km', dolzina=D('1'))


# Poslovna logika: cena postavke in vsote dokumenta

def test_cena_postavke_po_formuli_a():
    cena = cena_postavke(izmera_skupaj=D('20'), kolicina=D('1'), cena_na_enoto=D('10'), urna_postavka=D('25'),
                         stevilo_ur=D('8'), stevilo_delavcev=2, popust=D('0.10'), stopnja_ddv=D('0.22'))
    assert (cena['neto'], cena['ddv'], cena['koncna_cena']) == (D('540.00'), D('118.80'), D('658.80'))


def test_vsote_dokumenta_sestejejo_postavke():
    vsote = vsote_dokumenta([{'neto': D('100.00'), 'ddv': D('22.00')}, {'neto': D('50.00'), 'ddv': D('4.75')}])
    assert vsote == {'neto': D('150.00'), 'ddv': D('26.75'), 'skupaj': D('176.75')}


# Validacije

def test_decimalni_niz_je_sprejet():
    assert plain_decimal('12.50') == '12.50'


@pytest.mark.parametrize('vrednost', ['1e3', '-5', ' 1', 12.5])
def test_neveljaven_decimalni_vnos_je_zavrnjen(vrednost):
    with pytest.raises(ValueError):
        plain_decimal(vrednost)


# API končne točke

def test_health_vrne_ok():
    odgovor = client.get('/api/health')
    assert odgovor.status_code == 200 and odgovor.json()['status'] == 'ok'


def test_poslovni_zahtevek_brez_prijave_vrne_401():
    assert client.get('/api/me').status_code == 401


def test_kalkulator_zavrne_negativno_kolicino():
    odgovor = client.post('/api/demo/calculate', json={'quantity': -1, 'unit_cost': '1', 'unit_price': '2'})
    assert odgovor.status_code == 422
