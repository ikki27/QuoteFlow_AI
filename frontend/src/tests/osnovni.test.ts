import { describe, expect, it } from 'vitest';
import { fraction, percentValue } from '../features/items/percent';

describe('pretvorba odstotkov', () => {
  it('odstotek iz obrazca pretvori v delež za API', () => {
    expect(fraction('22')).toBe('0.22');
  });

  it('prazen vnos pomeni 0', () => {
    expect(fraction(null)).toBe('0');
    expect(fraction('')).toBe('0');
  });

  it('decimalni odstotek ohrani natančnost', () => {
    expect(fraction('9.5')).toBe('0.095');
  });

  it('delež iz API pretvori v odstotek za prikaz', () => {
    expect(percentValue('0.22')).toBe('22');
  });

  it('pretvorba tja in nazaj vrne isto vrednost', () => {
    expect(percentValue(fraction('12.5'))).toBe('12.5');
  });
});
